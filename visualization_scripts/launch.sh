#!/usr/bin/bash

# 1. start Cytoscape Application
cyto=$(python find_Cytoscape.py 2>&1)
echo $cyto
start $cyto

# 2. assert Cytoscape is running 
python check_process.py
echo "checkpoint passed, continuing script"