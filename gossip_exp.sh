#!/bin/bash 
>cav_tcgen/detailed_exetime_gossip.txt
>cav_tcgen/overview_exetime_gossip.txt

for i in `seq 2 $2`;
do
	cd cav_tcgen
	python $1.py $i
	cd ..
	python main.py n cav_tcgen/$1 | tee cav_tcgen/temp.txt
	Ptime=`cat cav_tcgen/temp.txt | grep 'Parser Performance' | awk '{print $4}'`
	Cstr=`cat cav_tcgen/temp.txt | grep 'Construction Performance' | awk '{print $5}'`
	PGstr=`cat cav_tcgen/temp.txt | grep 'PGSolver Performance' | awk '{print $4}'`
	EmC=`cat cav_tcgen/temp.txt | grep 'Non-Emptiness performance' | awk '{print $4}'`
	ToT=`cat cav_tcgen/temp.txt | grep 'Total performance' | awk '{print $4}'`
	GLTLS=`cat cav_tcgen/temp.txt | grep 'Kripke states' | awk '{print $3}'`
	GLTLE=`cat cav_tcgen/temp.txt | grep 'Kripke edges' | awk '{print $3}'`
	GParS=`cat cav_tcgen/temp.txt | grep 'GPar states' | awk '{print $3}'`
	GParE=`cat cav_tcgen/temp.txt | grep 'GPar edges' | awk '{print $3}'`
	TTPGS=`cat cav_tcgen/temp.txt | grep 'Max TTPG states' | awk '{print $4}'`
	TTPGE=`cat cav_tcgen/temp.txt | grep 'Max TTPG edges' | awk '{print $4}'`

	echo "$i;$Ptime;$Cstr;$PGstr;$EmC;$ToT;$GLTLS;$GLTLE;$GParS;$GParE;$TTPGS;$TTPGE " | tee -a cav_tcgen/detailed_exetime_gossip.txt
	echo "$i;$GLTLS;$GLTLE;$GParS;$GParE;$ToT" | tee -a cav_tcgen/overview_exetime_gossip.txt
done
