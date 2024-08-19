#!/bin/sh
set -eu

(cd ltl2ba && make clean && make)

[ ! -d temp ] || rm -rf temp
[ ! -d pgsolver ] || rm -rf pgsolver
mkdir -p temp

unzip pgsolver
eval $(opam config env)
opam install ocamlbuild ocamlfind ounit TCSLib extlib ocaml-sat-solvers minisat
cd pgsolver
echo "A" | ocaml setup.ml -configure
ocaml setup.ml -build

echo "     /\__/\      "
echo "    / o o \     "
echo "   / > ^ < \    "
echo "  (  /   \  )   "
echo "   \     /     "
echo "    \___/      "
echo "Hope the installation went smoothly. Have fun exploring!"