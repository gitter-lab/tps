# TPS Pipeline

**TPS workflow overview**

![Alt Text](https://github.com/ajshedivy/tps/blob/visualization_v2/workflow/TPS_workflow.png)

The TPS/workflow module utilizes the TPS repository structure in order to run the TPS software end-to-end in order to produce Cytoscape sessions. 

## Documentation

- `TPS.sh`
  - Runs TPS software 
  - sets up and initializes workspace environment `py2cyto_envirnment`
  - calls driver script `main.py`

- `main.py`
  - redirects TPS output files
  - calls utility functions for processing network annotations
  - calls visualization utilities
  
- `visualization_utilities.py`
  - utility functions used for creating cyREST client 
  - import ooutput groah files, style and annotation into Cytoscape
  - TODO : search machine for Cytoscape executable
  
- `table_refactor.py`
  - helper methods of reformatting annotations data


## Usage

In order to run pipeline, call

`bash TPS.sh` 

from workflow directory

***Note**: within `main.py`, change this [line](https://github.com/ajshedivy/tps/blob/visualization_v2/workflow/main.py#L62) to the install directory of Cytoscape

Example: `users/programs/Cytoscape_v3.7.1`

## Output 

With folder `TPS/results`, a time stamped folder is created with the following files:
* Cytoscape session file
* annotations data CSV
* orginal annotations file (no refactoring)
