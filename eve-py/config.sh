#!/bin/sh
set -eu

(cd ltl2ba && make clean && make)

[ ! -d temp ] || rm -rf temp
[ ! -d pgsolver-master ] || rm -rf pgsolver-master
mkdir -p temp

unzip pgsolver-master
eval $(opam config env)
opam install ocamlbuild ocamlfind ounit TCSLib extlib ocaml-sat-solvers minisat
cd pgsolver-master
echo "A" | ocaml setup.ml -configure
ocaml setup.ml -build
