#!/usr/bin/env/bash

#conda init bash
echo "----------------------------starting script----------------------------"

echo "-move to TPS base directory to run TPS"

echo $0

full_path=$(realpath $0)
echo $full_path

work_dir=$(dirname $full_path)
echo $work_dir

tps_dir=$(dirname $work_dir)
echo $tps_dir

cd $tps_dir

# "defualt TPS params"
./scripts/run \
   --network data/networks/input-network.tsv \
   --timeseries data/timeseries/median-time-series.tsv \
   --firstscores data/timeseries/p-values-first.tsv \
   --prevscores data/timeseries/p-values-prev.tsv \
   --partialmodel data/resources/kinase-substrate-interactions.sif \
   --peptidemap data/timeseries/peptide-mapping.tsv \
   --source EGF_HUMAN \
   --threshold 0.01

cd $work_dir



echo "-activate TPS environment"
eval "$(conda shell.bash hook)"
conda activate py2cyto_environment

#echo "check environment"
if [ $? -ne 0 ]; then
   echo "-environment does not exit"
	echo "-creating TPS environment"
	conda env create -f minimal_env.yml
	conda activate py2cyto_environment
fi
echo "-environment activated"

python main.py

echo "-end script"