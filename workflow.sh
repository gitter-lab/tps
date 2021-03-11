#!/bin/bash

echo "activate TPS environment"
eval "$(conda shell.bash hook)"
conda activate tps_workflow

if [ $? -ne 0 ]; then
   	echo "environment does not exist"
	echo "creating TPS environment"
	conda env create -f workflow/minimal_env.yml
	conda activate tps_workflow
fi
echo "environment activated"
 
python tps_runner.py --config $1 --execute $2 
