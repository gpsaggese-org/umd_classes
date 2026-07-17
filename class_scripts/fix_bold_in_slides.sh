#!/usr/bin/env bash
# Replace **Tag** bold labels with @Tag@ for the canonical slide/lecture tag
# set (see "### Tags" in .claude/skills/slides.rules.md).
set -euo pipefail

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <file> [<file> ...]" >&2
    exit 1
fi

perl -i -pe '
    BEGIN {
        @tags = (
            "Definition", "Question", "Goal", "Assumptions", "Problem",
            "(Naive) Solution", "Solution", "Pros", "Cons", "Example",
            "Intuition", "Key idea", "Remark", "Fact", "Theorem", "Proof",
            "Proposition", "Lemma", "Claim", "Algorithm", "Input", "Output",
            "Limitations", "Counterexample",
        );
    }
    for my $tag (@tags) {
        my $q = quotemeta($tag);
        my $repl = "\@" . $tag . "\@";
        s/\*\*$q\*\*/$repl/g;
    }
' "$@"
