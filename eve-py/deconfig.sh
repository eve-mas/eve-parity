#!/bin/sh

cd ltl2ba
make clean
cd ..

if [ -d "temp" ]; then
	rm -rf temp
fi

if [ -d "pgsolver-master" ]; then
	rm -rf pgsolver-master
fi
