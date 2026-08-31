# -*- coding: utf-8 -*-
"""Shared test helpers: run main.py as a subprocess (it relies on module-level
globals reset per run, e.g. parser tables, so in-process re-import is not
safe across multiple invocations) and parse its stdout the same way the
golden fixtures were captured."""

import json
import os
import re
import subprocess
import sys

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES_DIR = os.path.join(os.path.dirname(SRC_DIR), "examples")
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(TESTS_DIR, "golden_examples.json")) as f:
    GOLDEN = json.load(f)


def run_main(problem, example, extra_args=()):
    """Runs `python main.py <problem> ../examples/<example> -v [extra_args]`
    from eve-py/src, exactly as a user would from the README, and parses the
    same fields the golden fixtures record."""
    example_path = os.path.join(EXAMPLES_DIR, example)
    cmd = [sys.executable, "main.py", problem, example_path, "-v"] + list(extra_args)
    proc = subprocess.run(
        cmd, cwd=SRC_DIR, capture_output=True, text=True, timeout=120)
    return parse_output(proc.stdout, proc.returncode)


def parse_output(text, exit_code):
    entry = {"exit": exit_code}
    for key, pattern in [
        ("kripke_states", r"Kripke states (\d+)"),
        ("kripke_edges", r"Kripke edges (\d+)"),
        ("gpar_states", r"GPar states (\d+)"),
        ("gpar_edges", r"GPar edges (\d+)"),
    ]:
        m = re.search(pattern, text)
        if m:
            entry[key] = int(m.group(1))
    m = re.search(r">>> (YES|NO),", text)
    if m:
        entry["verdict"] = m.group(1)
    entry["raw"] = text
    return entry
