# eve-parity
Equilibrium Verification Environment

__EVE__ (Equilibrium Verification Environment) is a formal verification tool for the automated analysis of temporal equilibrium properties of concurrent and multi-agent systems represented as multi-player games. Systems are modelled using the Simple Reactive Module Language (SRML) as a collection of independent system components (players/agents in a game), which are assumed to have goals expressed using Linear Temporal Logic (LTL) formulae. In particular, __EVE__ checks for the existence of Nash equilibria in such systems and can be used to do rational synthesis and verification automatically.

__EVE__ has been tested on the following platforms:
- Fedora
- Ubuntu

## Prerequisites
1. python 2.x
2. IGraph version 0.7 (http://igraph.org/python/) (version 0.6 or older does not work)
	You need to have a C/C++ compiler installed on your machine.
	For Ubuntu: if needed 'sudo apt-get install -y libigraph0-dev'
3. Cairo (https://cairographics.org/download/)
	or from sourcecode (https://cairographics.org/releases/) --MacOS usually runs into trouble with auto install:
		- uncompress/unzip the source code folder
		- go inside the folder
		- run on terminal: 
				[your pc]$ ./configure --prefix=/usr/local --disable-dependency-tracking
				[your pc]$ make install
				install pkg-config if needed

4. OCaml version 4.03.x or later (https://ocaml.org/docs/install.html)
5. OPAM (https://opam.ocaml.org/doc/Install.html)
	can be installed from binaries (download from https://github.com/ocaml/opam/releases)
	or from source code (download from https://github.com/ocaml/opam/releases)
		- uncompress/unzip the source code folder
		- go inside the folder
		- follow installation instructions on README file and dont forget to initalise OPAM with current installation of OCaml (https://opam.ocaml.org/doc/Usage.html)
	Make sure OCaml is version 4.03.x or later before running config

## Configurations
1. Make sure you have all of the prerequisites
2. Go inside eve-py folder
3. Run shell script ./config.sh
   Make sure OCaml is version 4.03.x or later before running config.sh
   If you have OPAM installed in your machine, you can upgrade OCaml by executing these in terminal:
	- opam update
	- opam upgrade
	- opam switch 4.03.0

## How to use
- usage:

  $ main.py [problem] [path/name of the file] [options]

- List of problems:
   
   `a` 	 Parameter to solve A-Nash
   
   `e` 	 Parameter to solve E-Nash
   
   `n` 	 Parameter to solve Non-Emptiness
   
- List of optional arguments:
   
   `-d`	 Option to draw the structures

- Example:

   `$ main.py a .../examples/a-nash_1 -d` solves the A-Nash problem and draws the structures
