# -*- coding: utf-8 -*-
"""Regression test: every existing example under every applicable problem
letter (e/a/n) must keep producing the same verdict and the same reachable
arena/parity-game sizes across the Spot migration and the frontier/O(1)
performance ports. `golden_examples.json` was captured from the pre-change
code (ltl2nbw/nbw2dpw pipeline, unoptimized Arena2LTS/convertG sweeps) and
must not need updating by any later commit in this series -- if it does,
that commit changed observable behaviour, which is the one thing the
Spot/perf ports are not supposed to do."""

import pytest

from conftest import GOLDEN, run_main

CASES = [
    (example, problem)
    for example, problems in GOLDEN.items()
    for problem in problems
]


@pytest.mark.parametrize("example,problem", CASES)
def test_example_matches_golden(example, problem):
    expected = GOLDEN[example][problem]
    actual = run_main(problem, example)
    assert actual["exit"] == expected["exit"], actual["raw"]
    for key in ("kripke_states", "kripke_edges", "gpar_states", "gpar_edges", "verdict"):
        if key in expected:
            assert actual.get(key) == expected[key], (
                "%s/%s: expected %s=%r, got %r\n%s"
                % (example, problem, key, expected[key], actual.get(key), actual["raw"]))
