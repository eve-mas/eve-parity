#!/bin/sh

cd ltl2ba
make clean
cd ..

if [ -d "temp" ]; then
	rm -rf temp
fi

if [ -d "pgsolver" ]; then
	rm -rf pgsolver
fi
