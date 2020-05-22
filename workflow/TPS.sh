#!/usr/bin/env/bash

#conda init bash
echo "----------------------------starting script----------------------------"
echo $1

# FILE=$1
# if [ -f "$FILE" ]; then
# 	echo "-$FILE exists"
# else 
# 	echo "-$FILE does not exist"
# 	exit
# fi
workflow="\workflow"
tps=$1
c="${tps}${workflow}"
echo "${c}"

cd $1

./scripts/run \
   --network data/networks/input-network.tsv \
   --timeseries data/timeseries/median-time-series.tsv \
   --firstscores data/timeseries/p-values-first.tsv \
   --prevscores data/timeseries/p-values-prev.tsv \
   --partialmodel data/resources/kinase-substrate-interactions.sif \
   --peptidemap data/timeseries/peptide-mapping.tsv \
   --source EGF_HUMAN \
   --threshold 0.01

cd $c




eval "$(conda shell.bash hook)"
conda activate py2cyto_environment

#echo "check environment"
if [ $? -ne 0 ]; then
	echo "-creating py2cyto environment"
	conda env create -f minimal_env.yml
	conda activate py2cyto_environment
fi
echo "-environment activated"

python main.py

echo "-end script"