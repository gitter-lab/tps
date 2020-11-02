import yaml
import pprint
import sys
import subprocess
import os
import csv
import time
import pandas as pd
from workflow.table_generation import PrepTemporalCytoscapeTPS
from workflow.table_refactor import refactor_col_delim
from workflow.visualization_utilities import vis, find_path, process_exists
from workflow.parser import Parser
from workflow.visualization import Visualization
from requests.exceptions import ConnectionError as CE
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError




def main(args):

    CONFIG = args[1]
    config = os.path.abspath(CONFIG)

    with open(config) as c:
        params = yaml.load(c, Loader = yaml.FullLoader)

    parser = Parser()
    viz_engine  = Visualization()
    outputs, out_folder, label = parser.parse(config, params)
    annot, style = viz_engine.generate_annotations(outputs, params, out_folder)

    print("OUTPUTS_LIST: ", outputs)


    CYTOSCAPE = "Cytoscape.exe"
    DIRNAME = params[0]['Cytoscape']["path"]
    OUTPUT_FILE = os.path.join(out_folder, label+"-output.sif")
    outStyleFile = style
    REFACTORED_ANNOTATIONS = annot
    SAVE_FILE = os.path.join(out_folder, params[0]['Cytoscape']["session"])

    print("CYTOSCPAPE: ", CYTOSCAPE)
    print("DIRNAME: ", DIRNAME)
    print("OUTPUT: ", OUTPUT_FILE)
    print("annotations: ", REFACTORED_ANNOTATIONS)
    print("SAVE_FILE: ", SAVE_FILE)


     # check if Cytoscape is running
    is_running = process_exists('Cytoscape.exe')

    if (is_running == False):
        print("---Cytoscape not running")

        # find path to Cytoscape on machine
        cyto_path = find_path(CYTOSCAPE, DIRNAME)

        # open Cytoscape
        p = subprocess.Popen(cyto_path)

    else:

        # continue on
        print("---Cytoscape running")

    # call vis fuction to load input files in Cytoscape session
    # catch errors: ConnectionError, JSONDecoderError
    connection_count = 0
    JSON_count = 0
    http_count = 0
    switch = False
    start = time.time()
    while switch is False:
        try:
            
            # run visualization function
            vis(OUTPUT_FILE, outStyleFile, REFACTORED_ANNOTATIONS, SAVE_FILE)

            # flip switch value
            switch = True

        except CE as e:

            # requests.ConnectionError caught if connection cannot be made with Cytoscape Server
            connection_count += 1
            time.sleep(2)
            switch = False
            continue

        except JSONDecodeError as e:

            # error thorwn from trying to create CyClient
            JSON_count += 1
            time.sleep(2)
            switch = False
            continue
        except HTTPError as e :
            http_count+=1
            time.sleep(2)
            switch = False
    end = time.time()
    print("---time elapsed: ", end - start)

    print("---Finish loading output file and style file")






if __name__ == "__main__":
    main(sys.argv)

