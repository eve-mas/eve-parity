# EVE
Equilibrium Verification Environment

__EVE__ (Equilibrium Verification Environment) is a formal verification tool for the automated analysis of temporal equilibrium properties of concurrent and multi-agent systems represented as multi-player games. Systems are modelled using the Simple Reactive Module Language (SRML) as a collection of independent system components (players/agents in a game), which are assumed to have goals expressed using Linear Temporal Logic (LTL) formulae. In particular, __EVE__ checks for the existence of Nash equilibria in such systems and can be used to do rational synthesis and verification automatically.

## EVE ONLINE
__EVE__ can be used via webservice from http://eve.cs.ox.ac.uk/eve

## PUBLICATION
- J. Gutierrez, M. Najib, G. Perelli, and M. Wooldridge. [__Automated Temporal Equilibrium Analysis: Verification and Synthesis of Multi-Player Games__](https://doi.org/10.1016/j.artint.2020.103353). In *Artificial Intelligence*, 2020. [PDF](aij20.pdf)

- J. Gutierrez, M. Najib, G. Perelli, and M. Wooldridge. [__EVE: A Tool for Temporal Equilibrium Analysis__](https://doi.org/10.1007/978-3-030-01090-4_35). In *Proceedings of the 16th International Symposium on Automated Technology for Verification and Analysis (ATVA-2018)*, Los Angeles, October 2018. [PDF](atva18.pdf)

__EVE__ has been tested on the following platforms:
1. Fedora
2. Ubuntu

__EVE__ is also available preinstalled in Open Virtual Appliance (OVA) image running Lubuntu (lightweight Linux based on Ubuntu). This image (1.5 GB) can be downloaded from https://goo.gl/ikdSnw and can be directly run on VirtualBox (https://www.virtualbox.org/).

***
## INSTALLATION

### Prerequisites
1. python 3.x
2. OPAM  (https://opam.ocaml.org/doc/Install.html) + OCaml version 4.03.x or later (https://ocaml.org/docs/install.html).
   To install OPAM (along with OCaml):
	- Fedora
		-  `sudo yum install patch`
		-  `sudo yum install m4`
		- `sudo wget https://raw.github.com/ocaml/opam/master/shell/opam_installer.sh -O - | sh -s /usr/local/bin`
		- `echo "y" | opam init`
		- ``eval `opam config env` `` 
	- Ubuntu
		+ `sudo apt-get install m4`
		+ `sudo wget https://raw.github.com/ocaml/opam/master/shell/opam_installer.sh -O - | sh -s /usr/local/bin`
		+ `echo "y" | opam init`
		+ ``eval `opam config env` ``
		
3. Cairo (https://cairographics.org/download/) or from sourcecode (https://cairographics.org/releases/). To install Cairo:
	- Fedora
		+ `sudo yum install cairo-devel`
		+ `sudo yum install pycairo`
	- Ubuntu
		+ `sudo apt-get install libcairo2-dev`
		+ `sudo apt-get install python-cairo`
		
4. IGraph version 0.7 (http://igraph.org/python/)
	- You need to have a C/C++ compiler installed on your machine.
	To install 
	- Fedora
		+ `sudo yum install python-igraph`
	- Ubuntu
		+ `sudo apt-get install python-igraph`

### Configurations
1. Make sure you have all of the prerequisites
2. Go inside eve-py folder
3. Run shell script **./config.sh** (you may need to run **chmod +x config.sh**)
   Make sure OCaml is version 4.03.x or later before running config.sh
***   

### How to use
- usage:
From  inside folder **eve-py/src** execute the following command:
` $ main.py [problem] [path/name of the file] [options]`

- List of problems:
   
   `a` 	 Parameter to solve A-Nash
   
   `e` 	 Parameter to solve E-Nash
   
   `n` 	 Parameter to solve Non-Emptiness
   
- List of optional arguments:
   
   `-d`	 Option to draw the structures
   
   `-v` Option to execute in verbose mode

- Example:

   `$ main.py a ../examples/a-nash_1 -d` solves the A-Nash problem and draws the structures
   
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
