# -*- coding: utf-8 -*-
"""Tests for the opt-in `--strategy-class memoryless` extension to n/e/a
(enumerate_profiles.py). Strictly opt-in: default behaviour (perfect-
recall, i.e. today's enash.py/anash.py/nonemptiness.py) is unchanged and
already covered by test_regression_examples.py."""

from conftest import run_main


def test_memoryless_non_emptiness_finds_equilibria():
    result = run_main("n", "contract_verification", extra_args=("--strategy-class", "memoryless"))
    assert result["exit"] == 0, result["raw"]
    assert ">>> YES, a pure-memoryless NE exists <<<" in result["raw"], result["raw"]
    assert "Total pure-memoryless profiles checked: 12" in result["raw"], result["raw"]
    assert "Pure-memoryless NE found: 7" in result["raw"], result["raw"]


def test_memoryless_a_nash_matches_property_in_all_ne():
    # Contract Verification Game: not every pure-memoryless NE satisfies
    # the declared system property (some NE reach sCA, where phi fails),
    # so this must report NO.
    result = run_main("a", "contract_verification", extra_args=("--strategy-class", "memoryless"))
    assert result["exit"] == 0, result["raw"]
    assert ">>> NO, the property is satisfied in ALL pure-memoryless NE <<<" in result["raw"], result["raw"]


def test_memoryless_e_nash_matches_property_in_some_ne():
    result = run_main("e", "contract_verification", extra_args=("--strategy-class", "memoryless"))
    assert result["exit"] == 0, result["raw"]
    assert ">>> YES, the property is satisfied in some pure-memoryless NE <<<" in result["raw"], result["raw"]


def test_strategy_class_perfect_recall_rejected_for_problem_m():
    result = run_main("m", "contract_verification", extra_args=(
        "-p", "tests/fixtures/A_deliver_approve_reject.json",
        "--strategy-class", "perfect-recall",
    ))
    # printhelp() calls a bare sys.exit() (exit code 0) after printing the
    # error, so the error text itself is the only reliable signal here.
    assert "not supported for problem 'm'" in result["raw"], result["raw"]
