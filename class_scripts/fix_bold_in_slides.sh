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
            "(Naive) Solution",
            "Algorithm",
            "Applications",
            "Approach",
            "Assumptions",
            "Claim",
            "Concept",
            "Cons",
            "Counterexample",
            "Definition",
            "Example",
            "Fact",
            "Goal",
            "Input",
            "Intuition",
            "Key idea",
            "Lemma",
            "Limitations",
            "Output",
            "Problem",
            "Proof",
            "Proposition",
            "Pros",
            "Question",
            "Remark",
            "Solution",
            "Theorem"
        );
    }
    for my $tag (@tags) {
        my $q = quotemeta($tag);
        my $repl = "\@" . $tag . "\@";
        s/\*\*$q\*\*/$repl/g;
    }
' "$@"
