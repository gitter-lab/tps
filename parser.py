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

from requests.exceptions import ConnectionError as CE
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

class Parser:
    def parse(self, config, params):

        '''
        - parse input config file 
        - build TPS call 
        - call TPS 
        - gather outputs 
        - return:
            - list of outputs 
            - output_folder
            - out_label

      
        '''

        args = ['--network', \
        '--timeseries', \
        '--firstscores', \
        '--prevscores', \
        '--partialmodel', \
        '--peptidemap', \
        '--source',    \
        '--threshold'] 

        # config = os.path.abspath(config)
        # with open(config) as c:
        #     params = yaml.load(c, Loader = yaml.FullLoader)

        tps_paramS = []

        # # grab TPS params 
        build = []
        OUT_FOLDER = os.path.dirname(os.path.abspath(__file__))
        OUT_LABEL = ""
        build.extend(["bash", "./scripts/run"])
        for key, val in params[1]["TPS"][0]["required"].items():
            if key == "outlabel":
                OUT_LABEL = str(val)
            k = "--" + key
            build.extend([k, str(val)])

        for key, val in params[1]["TPS"][1]["optional"].items():
            if key == "outfolder":
                if val == "":
                    pass
                else:
                    OUT_FOLDER = os.path.abspath(val)
            if val == "":
                pass
            else:
                k = "--" + key
                build.extend([k, str(val)])
        
        
        print("outfolder switch {}".format(OUT_FOLDER))
        print("OUTLABEL: ", OUT_LABEL)

        process = subprocess.run(
            build,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # check output 

        outputs = str(subprocess.check_output(["ls", "-d", str(OUT_LABEL)+"*"], cwd=OUT_FOLDER), encoding= "utf-8").strip().split()
        outputs.append(OUT_LABEL)

        return outputs, OUT_FOLDER, OUT_LABEL

class Visualization:

    def refactor(self, outFile, out_folder):
            '''

            refactor annotations 


            '''

            ANNOTATIONS_FILE = outFile
            print("---absolute annotations path: ", ANNOTATIONS_FILE)

            # * Prepare data and directories
            data_delim = pd.read_csv(ANNOTATIONS_FILE, delimiter='\t').drop('Unnamed: 19', 1)
            temp_d = data_delim
            cols = data_delim.columns.values[3:]
            for col in cols:
                data_delim[col] = refactor_col_delim(temp_d, col)

            new_file2 = os.path.join(out_folder, 'annotations_data.csv')
            new_data = os.path.join(out_folder, 'refactored_annotations.txt')
            data_delim.to_csv(new_file2, mode='w', index=False)

            csv_file2 = new_file2
            txt_file2 = new_data
            with open(txt_file2, "a") as my_output_file:
                with open(csv_file2, "r") as my_input_file:
                    [my_output_file.write("\t".join(row)+'\n')
                    for row in csv.reader(my_input_file)]
                my_output_file.close()

            REFACTORED_ANNOTATIONS = txt_file2
            return os.path.join(out_folder, REFACTORED_ANNOTATIONS)

    def generate_annotations(self, outputs, params, out_folder):
        '''

        takes outputs from parse and generates orginal annotations 


        '''
        windowsFile = os.path.join(out_folder, outputs[-1]+'-activity-windows.tsv')
        networkFile = os.path.join(out_folder, outputs[-1]+'-output.sif')
        outFile = os.path.join(out_folder, params[2]["Annotations"]["outAnnotFile"] + '.txt')
        styleFile = os.path.join(out_folder, params[2]["Annotations"]["outStyleFile"])

        pepsPerProt = PrepTemporalCytoscapeTPS(params[2]["Annotations"]["peptideMapFile"], 
                                            params[2]["Annotations"]["timeSeriesFile"], 
                                            params[2]["Annotations"]["peptideFirstScores"],
                                            params[2]["Annotations"]["peptidePrevScoreFile"], 
                                            windowsFile, 
                                            networkFile,
                                            params[2]["Annotations"]["goldStandardFile"], 
                                            params[2]["Annotations"]["pvalThresh"], 
                                            params[2]["Annotations"]["logTransform"], 
                                            params[2]["Annotations"]["styleTemplateFile"],
                                            outFile,
                                            styleFile,
                                            params[2]["Annotations"]["addZero"]) # don't provide logDefault
        return self.refactor(outFile, out_folder), styleFile


    


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


    #  # check if Cytoscape is running
    # is_running = process_exists('Cytoscape.exe')

    # if (is_running == False):
    #     print("---Cytoscape not running")

    #     # find path to Cytoscape on machine
    #     cyto_path = find_path(CYTOSCAPE, DIRNAME)

    #     # open Cytoscape
    #     p = subprocess.Popen(cyto_path)

    # else:

    #     # continue on
    #     print("---Cytoscape running")

    # # call vis fuction to load input files in Cytoscape session
    # # catch errors: ConnectionError, JSONDecoderError
    # connection_count = 0
    # JSON_count = 0
    # http_count = 0
    # switch = False
    # start = time.time()
    # while switch is False:
    #     try:
            
    #         # run visualization function
    #         vis(OUTPUT_FILE, outStyleFile, REFACTORED_ANNOTATIONS, SAVE_FILE)

    #         # flip switch value
    #         switch = True

    #     except CE as e:

    #         # requests.ConnectionError caught if connection cannot be made with Cytoscape Server
    #         connection_count += 1
    #         time.sleep(2)
    #         switch = False
    #         continue

    #     except JSONDecodeError as e:

    #         # error thorwn from trying to create CyClient
    #         JSON_count += 1
    #         time.sleep(2)
    #         switch = False
    #         continue
    #     except HTTPError as e :
    #         http_count+=1
    #         time.sleep(2)
    #         switch = False
    # end = time.time()
    # print("---time elapsed: ", end - start)

    # print("---Finish loading output file and style file")






if __name__ == "__main__":
    main(sys.argv)

