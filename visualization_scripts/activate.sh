#!/usr/bin/env/bash

#conda init bash
echo "starting script"
eval "$(conda shell.bash hook)"
conda activate py2cyto

echo "check enviornment"
if [ $? -ne 0 ]; then
	echo "creating py2cyto environment"
	conda env create -f environment.yml
	conda activate py2cyto
fi
echo "environment activated"

bash launch.sh

python visualize.py $1 $2
echo "end script"