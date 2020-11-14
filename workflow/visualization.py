


import sys
import subprocess
import os
import csv
import time
import pandas as pd
from workflow.table_generation import PrepTemporalCytoscapeTPS
from workflow.table_refactor import refactor_col_delim
from workflow.visualization_utilities import vis, find_path, process_exists

class Visualization:

    def __init__(self, params):
        self.params = params

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

            new_file2 = os.path.join(out_folder, self.params[2]["Annotations"]["outAnnotFile"] + '-annotations_data.csv')
            new_data = os.path.join(out_folder, self.params[2]["Annotations"]["outAnnotFile"] + '-refactored_annotations.txt')
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

    def generate_annotations(self, outputs, out_folder):
        '''

        takes outputs from parse and generates orginal annotations 


        '''
        print("=================================================")
        print("GENERATE ANNOTATIONS")
        windowsFile = os.path.join(out_folder, outputs[-1]+'-activity-windows.tsv')
        networkFile = os.path.join(out_folder, outputs[-1]+'-output.sif')
        outFile = os.path.join(out_folder, self.params[2]["Annotations"]["outAnnotFile"] + '.txt')
        styleFile = os.path.join(out_folder, self.params[2]["Annotations"]["outStyleFile"])

        pepsPerProt = PrepTemporalCytoscapeTPS(self.params[2]["Annotations"]["peptideMapFile"], 
                                            self.params[2]["Annotations"]["timeSeriesFile"], 
                                            self.params[2]["Annotations"]["peptideFirstScores"],
                                            self.params[2]["Annotations"]["peptidePrevScoreFile"], 
                                            windowsFile, 
                                            networkFile,
                                            self.params[2]["Annotations"]["goldStandardFile"], 
                                            self.params[2]["Annotations"]["pvalThresh"], 
                                            self.params[2]["Annotations"]["logTransform"], 
                                            self.params[2]["Annotations"]["styleTemplateFile"],
                                            outFile,
                                            styleFile,
                                            addZero=self.params[2]["Annotations"]["addZero"]) # don't provide logDefault
        return self.refactor(outFile, out_folder), styleFile