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
__EVE__ has been tested on the following platforms:
1. Fedora
2. Ubuntu

__EVE__ is also available preinstalled in Open Virtual Appliance (OVA) image running Lubuntu (lightweight Linux based on Ubuntu). This image (1.5 GB) can be downloaded from https://goo.gl/ikdSnw and can be directly run on VirtualBox (https://www.virtualbox.org/).

### Windows Users
Windows users can run EVE via WSL Ubuntu (https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-10#1-overview). You may need to disable sanboxing when initialising OPAM (see: https://stackoverflow.com/questions/54987110/installing-ocaml-on-windows-10-using-wsl-ubuntu-problems-with-bwrap-bubblewr).

## INSTALLATION

### Prerequisites
Before installing EVE, make sure you have the following prerequisites installed:
1. python 3.x
2. OPAM  (https://opam.ocaml.org/doc/Install.html) + OCaml version 4.03.0 >= and <= 4.07.0 (https://ocaml.org/docs/install.html). To see OCaml version `ocaml --version`.
   You may need to donwgrade your OCaml:
   	- Run `opam switch list`, and switch to an available version between 4.03.0 >= and <= 4.07.0.
   	- If there is no OCaml version between 4.03.0 >= and <= 4.07.0, run `opam switch create 4.07.0`
   	  
   To initialise OPAM (along with OCaml):
   	- `echo "y" | opam init`
	- ``eval `opam config env` ``		
4. Cairo (https://cairographics.org/download/) or Pycairo (https://pycairo.readthedocs.io/en/latest/index.html)
5. IGraph version 0.7 or later (http://igraph.org/python/)

### Configuration Steps
1. Ensure all prerequisites are installed.
2. Go inside eve-py folder
3. Run shell script **./config.sh** (you may need to run **chmod +x config.sh**)
   Make sure OCaml is version 4.03.0 >= and <= 4.07.0 before running config.sh
   
***   

### How to use
- usage:
From inside folder **eve-py/src** execute the following command:
` $ python main.py [problem] [path/name of the file] [options]`

- List of problems:
   
   `a` 	 Parameter to solve A-Nash
   
   `e` 	 Parameter to solve E-Nash
   
   `n` 	 Parameter to solve Non-Emptiness
   
- List of optional arguments:
   
   `-d`	 Option to draw the structures
   
   `-v` Option to execute in verbose mode

- Example:

   `$ python main.py a ../examples/a-nash_1 -d` solves the A-Nash problem and draws the structures. The drawing will be saved in the current (src) folder as `str.png`.
   
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
