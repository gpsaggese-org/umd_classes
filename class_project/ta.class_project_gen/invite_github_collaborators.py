#!/usr/bin/env python3
# repo_access_sync.py
"""
Declaratively sync repo collaborators from a CSV, with an ignore list.

CSV columns (header required): username,permission
Permissions: pull | triage | push | maintain | admin

Examples:
  export GITHUB_TOKEN=ghp_xxx   # or: gh auth login
  python repo_access_sync.py --repo OWNER/REPO --csv desired_access.csv --dry-run
  python repo_access_sync.py --repo OWNER/REPO --csv desired_access.csv \
      --ignore service-bot --ignore ownername \
      --ignore-file always_keep.txt
"""

from __future__ import annotations
import argparse
import csv
import logging
import os
import subprocess
from dataclasses import dataclass
from typing import Dict, Set, Iterable, Optional

from github import Github, GithubException, Auth

import helpers_root.helpers.hparser as hparser
import helpers_root.helpers.hdbg as hdbg

_LOG = logging.getLogger(__name__)

VALID_PERMS = {"pull", "triage", "push", "maintain", "admin"}


@dataclass(frozen=True)
class InviteInfo:
    permission: str
    invitation_id: int


def _get_token() -> Optional[str]:
    tok = os.getenv("GITHUB_TOKEN", "").strip()
    if tok:
        return tok
    try:
        tok = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
        if tok:
            return tok
    except Exception:
        pass
    _LOG.error("No token found. Set GITHUB_TOKEN or run `gh auth login`.")
    return None


def _connect(token: str) -> Github:
    auth = Auth.Token(token)
    base = os.getenv("GITHUB_API_URL", "").strip()
    return Github(base_url=base, auth=auth) if base else Github(auth=auth)


def _read_csv(path: str) -> Optional[Dict[str, str]]:
    desired: Dict[str, str] = {}
    try:
        with open(path, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            if not r.fieldnames or "Github Username" not in r.fieldnames or "Permission" not in r.fieldnames:
                _LOG.error("CSV must have columns: Github Username,Permission")
                return None
            for row in r:
                u = (row.get("Github Username") or "").strip()
                p = (row.get("Permission") or "").strip().lower()
                if not u:
                    continue
                if p not in VALID_PERMS:
                    _LOG.error("Invalid permission '%s' for '%s'. Allowed: %s", p, u, sorted(VALID_PERMS))
                    return None
                desired[u.lower()] = p
    except FileNotFoundError:
        _LOG.error("CSV file not found: %s", path)
        return None
    except Exception as e:
        _LOG.error("Error reading CSV '%s': %s", path, e)
        return None
    return desired


def _read_ignore(args) -> Set[str]:
    ignore: Set[str] = set(u.lower() for u in (args.ignore or []))
    if args.ignore_file:
        try:
            with open(args.ignore_file, "r", encoding="utf-8") as fh:
                for line in fh:
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    ignore.add(s.lower())
        except FileNotFoundError:
            _LOG.error("Ignore file not found: %s", args.ignore_file)
        except Exception as e:
            _LOG.error("Error reading ignore file '%s': %s", args.ignore_file, e)
    return ignore


def _fetch_repo(gh: Github, full: str):
    if "/" not in full:
        _LOG.error("--repo must be OWNER/REPO (got '%s')", full)
        return None
    try:
        return gh.get_repo(full)
    except GithubException as e:
        _LOG.error("Cannot access repo %s: %s", full, e)
        return None
    except Exception as e:
        _LOG.error("Unexpected error accessing repo %s: %s", full, e)
        return None


def _current_collaborators(repo) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for user in repo.get_collaborators():
        perm = repo.get_collaborator_permission(user)  # read|triage|write|maintain|admin
        perm_rest = {"read": "pull", "write": "push"}.get(perm, perm)
        out[user.login.lower()] = perm_rest
    return out


def _pending_invitations(repo) -> Dict[str, InviteInfo]:
    out: Dict[str, InviteInfo] = {}
    try:
        for inv in repo.get_pending_invitations():
            out[inv.invitee.login.lower()] = InviteInfo(
                permission=inv.permissions, invitation_id=inv.id
            )
    except GithubException:
        # Not all tokens can list invitations; ignore.
        pass
    return out


def _validate_users_exist(gh: Github, usernames: Iterable[str]) -> Set[str]:
    """
    Return the set of usernames (lowercased) that do NOT resolve on GitHub.
    """
    invalid: Set[str] = set()
    for u in usernames:
        try:
            gh.get_user(u)
        except GithubException:
            invalid.add(u)
        except Exception as e:
            _LOG.debug("Unexpected error validating user '%s': %s", u, e)
            invalid.add(u)
    return invalid


def _parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--repo", required=True, help="OWNER/REPO")
    parser.add_argument("--csv", required=True, help="CSV with username,permission")
    parser.add_argument("--dry-run", action="store_true", help="Print actions only, no changes")
    parser.add_argument(
        "--ignore",
        action="append",
        help="Username to never revoke (repeatable)",
        default=["aver81", "gsaggese", "indro"],
    )
    parser.add_argument(
        "--ignore-file",
        help="Path to a file with usernames to never revoke (one per line)",
        default=None,
    )
    hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    hdbg.init_logger(verbosity=args.log_level, use_exec_path=True)

    token = _get_token()
    if not token:
        _LOG.error("Aborting: missing GitHub token.")
        return

    gh = _connect(token)

    repo = _fetch_repo(gh, args.repo)
    if repo is None:
        _LOG.error("Aborting: unable to access target repo.")
        return

    desired = _read_csv(args.csv)
    if desired is None:
        _LOG.error("Aborting: CSV could not be processed.")
        return

    ignore = _read_ignore(args)
    current = _current_collaborators(repo)
    pending = _pending_invitations(repo)

    # Validate CSV usernames BEFORE computing removals to prevent accidental revokes on typos.
    invalid = _validate_users_exist(gh, desired.keys())
    if invalid:
        _LOG.error("CSV contains invalid GitHub usernames: %s", ", ".join(sorted(invalid)))
        _LOG.error("Aborting without changes.")
        return

    # Plan
    to_add: Dict[str, str] = {}
    to_update: Dict[str, str] = {}
    to_remove = []
    to_invite_update: Dict[str, str] = {}
    to_invite_cancel = []

    # Adds/updates/pending adjustments for desired users
    for user, want in desired.items():
        if user in current:
            if current[user] != want:
                to_update[user] = want
        elif user in pending:
            if pending[user].permission != want:
                to_invite_update[user] = want
        else:
            to_add[user] = want

    # Remove collaborators not in desired, but skip ignored
    for user in current:
        if user not in desired and user not in ignore:
            to_remove.append(user)

    # Cancel invites not in desired, but skip ignored
    for user in pending:
        if user not in desired and user not in ignore:
            to_invite_cancel.append(user)

    _LOG.info("=== PLAN ===")
    _LOG.info("Add: %s", to_add)
    _LOG.info("Update: %s", to_update)
    _LOG.info("Remove: %s", to_remove)
    _LOG.info("Invite-Update: %s", to_invite_update)
    _LOG.info("Invite-Cancel: %s", to_invite_cancel)
    _LOG.info("Ignore (no revoke): %s", sorted(ignore))
    _LOG.info("Dry-run: %s", args.dry_run)
    _LOG.info("============")

    if args.dry_run:
        _LOG.info("Dry-run enabled. No changes applied.")
        return

    # Apply
    for user, perm in to_add.items():
        _LOG.info("[ADD] %s -> %s", user, perm)
        try:
            repo.add_to_collaborators(user, permission=perm)
        except GithubException as e:
            _LOG.error("Failed to add %s: %s", user, e)

    for user, perm in to_update.items():
        _LOG.info("[UPDATE] %s -> %s", user, perm)
        try:
            repo.add_to_collaborators(user, permission=perm)  # re-add updates perm
        except GithubException as e:
            _LOG.error("Failed to update %s: %s", user, e)

    for user, perm in to_invite_update.items():
        _LOG.info("[INVITE-UPDATE] %s -> %s", user, perm)
        try:
            # cancel existing invite then re-invite
            for inv in repo.get_pending_invitations():
                if inv.invitee.login.lower() == user:
                    repo.delete_invitation(inv)
                    break
            repo.add_to_collaborators(user, permission=perm)
        except GithubException as e:
            _LOG.error("Failed to update invitation for %s: %s", user, e)

    for user in to_invite_cancel:
        _LOG.info("[INVITE-CANCEL] %s", user)
        try:
            for inv in repo.get_pending_invitations():
                if inv.invitee.login.lower() == user:
                    repo.delete_invitation(inv)
                    break
        except GithubException as e:
            _LOG.error("Failed to cancel invitation for %s: %s", user, e)

    for user in to_remove:
        _LOG.info("[REMOVE] %s", user)
        try:
            repo.remove_from_collaborators(user)
        except GithubException as e:
            _LOG.error("Failed to remove %s: %s", user, e)


if __name__ == "__main__":
    _main(_parse())
