#!/bin/bash

echo "activate TPS environment"
eval "$(conda shell.bash hook)"
conda activate py2cyto_environment

#echo "check environment"
if [ $? -ne 0 ]; then
   echo "environment does not exist"
	echo "creating TPS environment"
	conda env create -f workflow/minimal_env.yml
	conda activate py2cyto_environment
fi
echo "environment activated"
 
python tps_runner.py --config $1 --execute $2 

echo "end script"