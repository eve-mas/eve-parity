# -*- coding: utf-8 -*-
"""GPar (parity-game product) size stability, pinned from the Spot migration
onward. Unlike golden_examples.json's arena sizes/verdicts (pinned since
before Spot), GPar sizes were expected to (and did) shrink when Spot
replaced the old ltl2nbw/nbw2dpw pipeline -- see test_regression_examples.py's
module docstring. From this baseline forward, though, GPar size is exactly
what the frontier/O(1)-lookup performance port in convertG/convertG_cgs
must NOT change: same fixpoint, same final vertex/edge set, just reached
without rescanning already-expanded vertices."""

import json
import os

import pytest

from conftest import TESTS_DIR, run_main

with open(os.path.join(TESTS_DIR, "golden_gpar_post_spot.json")) as f:
    GPAR_GOLDEN = json.load(f)

CASES = [
    (example, problem)
    for example, problems in GPAR_GOLDEN.items()
    for problem in problems
]


@pytest.mark.parametrize("example,problem", CASES)
def test_gpar_size_unchanged(example, problem):
    expected = GPAR_GOLDEN[example][problem]
    actual = run_main(problem, example)
    for key in ("gpar_states", "gpar_edges"):
        assert actual.get(key) == expected[key], (
            "%s/%s: expected %s=%r, got %r\n%s"
            % (example, problem, key, expected[key], actual.get(key), actual["raw"]))
