import sys
import subprocess
import os
import csv
import time
import pandas as pd
import numpy as np
from workflow.table_generation import PrepTemporalCytoscapeTPS
from workflow.visualization_utilities import vis, find_path, process_exists

class Visualization:

    def __init__(self, params):
        self.params = params

    def refactor_col(self, annotations_df, col_name):
        '''
        Function used for changing column types of annotations df
        for Sig and Insig peptide changes

        :param annotations_df (DataFrame): global annptaions dataframe 
        :param col_name (String): name of column to refactor

        '''
        new_col = []
        for row in annotations_df[col_name]:

            if np.all(pd.isnull(row)):
                new_col.append(np.nan)
                continue
            elif row == "Not active":
                print("not active")
                new_col.append(row)
                continue
            else:
                temp_list = row.split(",")
                for num in range(len(temp_list)):
                    temp_list[num] = str(float(temp_list[num]))
                new_col.append("|".join(temp_list))
        
        new_df = pd.Series(new_col)
        return new_df

    def refactor(self, outFile, out_folder):
            '''
            refactor annotations

            '''
            ANNOTATIONS_FILE = outFile
            print("---absolute annotations path: ", ANNOTATIONS_FILE)

            # * Prepare data and directories
            data_delim = pd.read_csv(ANNOTATIONS_FILE, delimiter='\t')
            data_delim.drop(data_delim.columns[data_delim.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
            temp_d = data_delim
            cols = data_delim.columns.values[3:]
            for col in cols:
                data_delim[col] = self.refactor_col(temp_d, col)

            new_file = os.path.join(out_folder, self.params["Annotations"]["outAnnotFile"] + '-annotations_data.csv')
            new_data = os.path.join(out_folder, self.params["Annotations"]["outAnnotFile"] + '-refactored_annotations.txt')
            data_delim.to_csv(new_file, mode='w', index=False)

            csv_file = new_file
            txt_file = new_data
            with open(txt_file, "w") as my_output_file:
                with open(csv_file, "r") as my_input_file:
                    [my_output_file.write("\t".join(row)+'\n')
                    for row in csv.reader(my_input_file)]
                my_output_file.close()

            REFACTORED_ANNOTATIONS = txt_file
            return os.path.join(out_folder, REFACTORED_ANNOTATIONS)

    def generate_annotations(self, outputs, out_folder):
        '''

        takes outputs from parse and generates orginal annotations 


        '''
        print("=================================================")
        print("GENERATE ANNOTATIONS")
        windowsFile = os.path.join(out_folder, outputs[-1]+'-activity-windows.tsv')
        networkFile = os.path.join(out_folder, outputs[-1]+'-output.sif')
        outFile = os.path.join(out_folder, self.params["Annotations"]["outAnnotFile"] + '.txt')
        styleFile = os.path.join(out_folder, self.params["Annotations"]["outStyleFile"])

        pepsPerProt = PrepTemporalCytoscapeTPS(self.params["Annotations"]["peptideMapFile"], 
                                            self.params["Annotations"]["timeSeriesFile"], 
                                            self.params["Annotations"]["peptideFirstScores"],
                                            self.params["Annotations"]["peptidePrevScoreFile"], 
                                            windowsFile, 
                                            networkFile,
                                            self.params["Annotations"]["goldStandardFile"], 
                                            self.params["Annotations"]["pvalThresh"], 
                                            self.params["Annotations"]["logTransform"], 
                                            self.params["Annotations"]["styleTemplateFile"],
                                            outFile,
                                            styleFile,
                                            addZero=self.params["Annotations"]["addZero"]) # don't provide logDefault
        #return outFile, styleFile
        return self.refactor(outFile, out_folder), styleFile