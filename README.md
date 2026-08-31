# EVE
Equilibrium Verification Environment

__EVE__ (Equilibrium Verification Environment) is a formal verification tool for the automated analysis of temporal equilibrium properties of concurrent and multi-agent systems represented as multi-player games (see [rational verification](https://link.springer.com/article/10.1007/s10489-021-02658-y)). Systems/Games in EVE are modelled using the Simple Reactive Module Language (SRML) as a collection of independent system components (players/agents in a game). These components/players are assumed to have goals expressed using Linear Temporal Logic (LTL) formulae. __EVE__ checks for the existence of Nash equilibria in such systems and can be used to do rational synthesis and verification automatically.

We are always interested in improving EVE (e.g., faster techniques, new use cases, etc.). Please feel free to [contact us](mailto:m.najib@hw.ac.uk) for potential collaborations.

## EVE ONLINE
__EVE__ can be used via webservice from https://eve.cs.ox.ac.uk/eve

## PUBLICATION
- J. Gutierrez, M. Najib, G. Perelli, and M. Wooldridge. [__Automated Temporal Equilibrium Analysis: Verification and Synthesis of Multi-Player Games__](https://doi.org/10.1016/j.artint.2020.103353). In *Artificial Intelligence*, 2020. [PDF](aij20.pdf)

- J. Gutierrez, M. Najib, G. Perelli, and M. Wooldridge. [__EVE: A Tool for Temporal Equilibrium Analysis__](https://doi.org/10.1007/978-3-030-01090-4_35). In *Proceedings of the 16th International Symposium on Automated Technology for Verification and Analysis (ATVA-2018)*, Los Angeles, October 2018. [PDF](atva18.pdf)
***

## 
__EVE__ runs on Linux/UNIX platforms, e.g.,:
1. Fedora
2. Ubuntu
3. macOS

__EVE__ is also available preinstalled in Open Virtual Appliance (OVA) image running Lubuntu (lightweight Linux based on Ubuntu). This image (1.5 GB) can be downloaded from https://goo.gl/ikdSnw and can be directly run on VirtualBox (https://www.virtualbox.org/).

### Windows Users
Windows users can run EVE via WSL Ubuntu (https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview). You may need to disable sanboxing when initialising OPAM (see: https://stackoverflow.com/questions/54987110/installing-ocaml-on-windows-10-using-wsl-ubuntu-problems-with-bwrap-bubblewr).

## INSTALLATION

EVE's LTL-to-automaton conversion is built on [Spot](https://spot.lre.epita.fr/), whose Python bindings (`spot` + `buddy`) are native extensions built against one specific Python version. The most reliable way to install everything EVE needs -- Spot, its own pinned Python, and the other Python dependencies -- is a single dedicated Conda/Miniforge environment, described below. `pgsolver` (an external OCaml parity-game solver) is still required, but only for the `e`/`a`/`n` problems (and their `--strategy-class memoryless` variants) -- it is not needed for `m` (pure-memoryless profile checking).

### Recommended: Conda/Miniforge environment

**If you don't already have Conda:** install [Miniforge](https://github.com/conda-forge/miniforge) (community-maintained, conda-forge by default):
```bash
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash "Miniforge3-$(uname)-$(uname -m).sh"
```
Accept the license, let the installer initialise your shell, then open a new shell (or `source ~/.bashrc`).

**Create the environment** from the repository root:
```bash
cd eve-py
conda env create -f environment-spot.yml
conda activate eve-spot
```
This installs Python 3.12, `spot` (which brings its own `buddy` Python bindings -- nothing else to install for Buddy), `python-igraph`, `pytest`, and `ply` (a plain Python package `parsrml.py` needs to parse SRML model files). Do all of EVE's installation and every run inside this one environment; do not also `source`/activate a separate virtualenv at the same time.

### Additional prerequisites for E-Nash/A-Nash/Non-Emptiness (`e`/`a`/`n`)

These three problems (and `--strategy-class memoryless` for any of them) call the external OCaml parity-game solver [PGSolver](https://github.com/tcsprojects/pgsolver) for punishment-region computation. `m` (pure-memoryless profile checking) does not need any of this.

1. OPAM (https://opam.ocaml.org/doc/Install.html) + OCaml version 4.03.0 or later (https://ocaml.org/docs/install.html). To see OCaml version `ocaml --version`.
   To initialise OPAM (along with OCaml):
   	- `echo "y" | opam init`
	- ``eval `opam config env` ``
2. Cairo (https://cairographics.org/download/) or Pycairo (https://pycairo.readthedocs.io/en/latest/index.html) -- only needed for `-d` (drawing the structures).

### Configuration Steps
1. Activate the `eve-spot` conda environment above.
2. Ensure OPAM/OCaml is installed if you plan to use `e`/`a`/`n`.
3. Navigate to the `eve-py` folder.
4. Run the executable script **./config.sh** (you may need to run **chmod +x config.sh** first) to build PGSolver.
   Make sure OCaml is version 4.03.0 or later before running config.sh.

***

### How to use
- usage:
From inside folder **eve-py/src** execute the following command:
` $ python main.py [problem] [path/name of the file] [options]`

- List of problems:
   
   `a` 	 Parameter to solve A-Nash
   
   `e` 	 Parameter to solve E-Nash
   
   `n` 	 Parameter to solve Non-Emptiness

   `m` 	 Check a caller-supplied pure-memoryless strategy profile (requires `-p`; see "Pure-memoryless profile checking" below)
   
- List of optional arguments:
   
   `-d`	 Option to draw the structures
   
   `-v` Option to execute in verbose mode

   `-p <path>` Path to a profile JSON file (required for problem `m`)

   `-a <path>` Path to an optional alias JSON file for problem `m`, of the form `{"actions": {"<player>": {"<friendly name>": "<raw action id>"}}, "states": {"<friendly name>": "s<N>"}}`, letting a profile file and its report use human-chosen names instead of raw state/action identifiers

   `-j <path>` Path to write a machine-readable JSON result for problem `m`

   `--strategy-class {perfect-recall,memoryless}` Strategy class for `n`/`e`/`a` (default: `perfect-recall`, i.e. today's behaviour). `m` is always memoryless; `--strategy-class perfect-recall` is rejected for `m` rather than silently ignored.

- Example:

   `$ python main.py a ../examples/a-nash_1 -d` solves the A-Nash problem and draws the structures. The drawing will be saved in the current (src) folder as `str.png`.

   `$ python main.py m ../examples/contract_verification -p my_profile.json` checks whether `my_profile.json` is a pure-memoryless Nash equilibrium of `contract_verification`.

### Pure-memoryless profile checking

Problem `m` analyses one caller-supplied, complete **pure-memoryless** strategy profile: one legal action per player, at every state of the original game where that player has a real decision -- not only the states visited along the profile's own induced path. "Memoryless" here means literally `sigma_i : St -> Ac_i` over the vertices of the original game arena `St` (the Kripke/LTS structure `Arena2Kripke`/`Arena2LTS` build); it does **not** mean positional in a parity-automaton product. A strategy that is positional in the product of the arena with an LTL goal's deterministic parity automaton can still depend on that automaton's internal state -- which itself depends on history -- and would therefore correspond to a *history-dependent* strategy in the original game, not a memoryless one. `checkprofile.py` keeps these separate: a supplied profile's action for a state is looked up purely by that state's identity, and the parity-automaton product is used only to compute outcomes, never as the domain a policy is indexed by.

Given a profile, `m` reports:
- each player's own goal satisfaction and, if the SRML file declares a `property`, whether the induced outcome satisfies it;
- whether the profile is a Nash equilibrium against unilateral deviations in the same strategy class (pure memoryless);
- for every player who is losing, every alternative complete memoryless policy for that player that would make them win, with the complete witness policy (not just the resulting outcome).

This is a separate analysis mode from `e`/`a`/`n`'s existing perfect-recall rational verification: those solve parity games over the product of the arena with each player's goal automaton, so the strategies they reason about are effectively history-dependent in the original game. `--strategy-class memoryless` (see above) extends `n`/`e`/`a` themselves to ask the analogous question over *all* complete pure-memoryless profiles (by exhaustive enumeration), rather than over one caller-supplied profile.

EVE has no notion of how a candidate profile was produced -- hand-authored, synthesised, or supplied by an external agent or tool. It only checks the resulting profile against the game.

### Running experiments
1. Go to folder **eve-py/src/experiments**, there are 8 scripts (you may need to run **chmod +x <script_filename.sh>** to run these scripts):
	+ bisim_ne_emptiness.sh
	+ bisim_none_emptiness.sh
	+ gossip_protocol_emptiness.sh
	+ gossip_protocol_enash.sh
	+ gossip_protocol_anash.sh
	+ replica_control_emptiness.sh
	+ replica_control_enash.sh
	+ replica_control_anash.sh
2. Execute the script "experiment_name".sh using the command `./experiment_name.sh 8`
3. This will run the experiment "experiment_name" up until 8 steps.
4. The experiment results are reported in the generated file **exetime_experiment_name.txt** with the following respective values separated by semicolons:
	+ parser performance (ms)
	+ construction peformance (ms)
	+ PGSolver performance (ms)
	+ non-emptiness/E-Nash/A-Nash performance (ms)
	+ total number of parity game states
	+ total number of parity game edges
	+ maximum total number of sequentialised parity game states
	+ maximum total number of sequentialised parity game edges
	+ total time performance (ms)
