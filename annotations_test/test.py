import os
import pandas as pd
import numpy as np
from datetime import date
import subprocess
import sys
import time
import csv
sys.path.insert(1, os.path.abspath(".."))
import workflow.table_generation as table


def main():
    today = date.today()
    
    print(os.path.abspath('..'))
    baseDir = os.path.abspath(os.path.join('..'))
    tps_in_dir = os.path.join(baseDir, 'data', 'timeseries')
    print(baseDir)
    print(tps_in_dir)
    
    # workflow
    workflow = os.path.join(baseDir, 'workflow')
    
    # * Move files into directory
    output_sif_orig = os.path.join(workflow, 'output.sif')
    activity_tsv_orig = os.path.join(workflow, 'activity-windows.tsv')

    # * Gather data used to generate node anotations
    # Use the version with the header line
    pepMapFile = os.path.join(tps_in_dir, 'peptide-mapping.tsv')
    pepFirstFile = os.path.join(tps_in_dir, 'p-values-first.tsv')
    pepPrevFile = os.path.join(tps_in_dir, 'p-values-prev.tsv')
    print(pepMapFile)
    print(pepFirstFile)
    print(pepPrevFile)

    # Use the version for which log2 fold change has been precomputed
    timeSeriesFile = os.path.join(
        baseDir, 'data', 'timeseries', 'log2FoldChange011215.txt')
    #timeSeriesFile = r"C:\\Users\\ajshe\\Anaconda3\\envs\\py2cyto\\tps\\data\\timeseries\\log2FoldChange011215.txt"
    print(timeSeriesFile)

    windowsFile = os.path.join(baseDir, 'workflow', 'activity-windows.tsv')
    networkFile = os.path.join(baseDir, 'workflow', 'output.sif')
    print(windowsFile)
    print(networkFile)
    
     # Use the same EGFR gold standard for Olsen 2006 and Ale's data
    goldStandardFile = os.path.join(
        baseDir, 'data', 'resources', 'eight-egfr-reference-all.txt')

    styleTemplateFile = os.path.join(
        baseDir, 'notebooks', 'tps_style_template.xml')

    out_dir = os.path.join(baseDir, 'results', str(
        today) + '-and-wolf-yadlin-TPS-cytoscape')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print('Created {}'.format(out_dir))
    outFile = os.path.join(
        out_dir, 'wolf-yadlin-cytoscape-annotations-' + str(today) + '.txt')
    outStyleFile = os.path.join(out_dir, 'tps_style.xml')
    
    # * run Utility function
    pvalThresh = 0.01  # Same threhsold used in TPS
    logTransform = False
    pepsPerProt = table.PrepTemporalCytoscapeTPS(pepMapFile, timeSeriesFile, pepFirstFile,
                                           pepPrevFile, windowsFile, networkFile,
                                           goldStandardFile, pvalThresh, logTransform, styleTemplateFile,
                                           outFile,
                                           outStyleFile,
                                           addZero=True)  # don't provide logDefault
    
    


if __name__ == "__main__":
    main()
