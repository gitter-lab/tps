#!/usr/bin/bash

isRunning=$(python check_process.py 2>&1)
echo $isRunning
Return_true="True"

 
if [ "$isRunning" == "$Return_true" ];
then 
    echo "Cytoscape is running"
    exit 1
else 
    echo "find Cytoscape on machine"
    cyto=$(python find_Cytoscape.py 2>&1)
    printf "location of Cytoscape\n> "
    echo $cyto
    start $cyto
fi

