#!/bin/sh
cd ltl2ba
make clean
make
cd ..
if [ -d "temp" ]; then
	rm -rf temp
	mkdir temp
else
	mkdir temp
fi
if [ -d "pgsolver-master" ]; then
	rm -rf pgsolver-master
fi
unzip pgsolver-master
eval `opam config env`
opam install ocamlbuild ocamlfind ounit TCSLib extlib ocaml-sat-solvers minisat
cd pgsolver-master
echo "A" | ocaml setup.ml -configure
ocaml setup.ml -build
