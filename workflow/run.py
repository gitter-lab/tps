
from workflow.visualization_utilities import vis, find_path, process_exists
from workflow.table_generation import PrepTemporalCytoscapeTPS
import os
import pandas as pd

def main(args):

    '''
    run TPS
    gather input data
    prepare annotations file
    run visualization
    '''
    
    #* Run TPS!
    
    
    #* create Base directory
    baseDir = os.path.abspath(os.path.join('..'))
    tps_in_dir = os.path.join(baseDir, 'data', 'timeseries')
    tps_out_dir = os.path.join(baseDir, 'results', 'results_reproduce_egfr_tps_' + str(today))
    if not os.path.exists(tps_out_dir):
        os.makedirs(tps_out_dir)
        print('Created {}'.format(tps_out_dir))
    print(baseDir)
    print(tps_in_dir)
    print(tps_out_dir)
    
    # input args from command line
    OUTPUT_FILE = os.path.join(baseDir, 'workflow', 'output.sif')
    STYLE_FILE = os.path.join(baseDir, 'workflow', 'tps_style.xml')
    ANNOTATIONS_FILE = args[3]
    DIRNAME = r"C:\Users\ajshe\OneDrive\Documents\Comp_bio\Cytoscape_v3.7.1"
    CYTOSCAPE = 'Cytoscape.exe'

    if OUTPUT_FILE.lower().endswith(".sif"):
        print ("file has valid extention")
    else:
        print ("invalid extension on output file: ", OUTPUT_FILE)
        sys.exit()

    # get absolute paths if nessesay
    OUTPUT_FILE = os.path.abspath(OUTPUT_FILE)
    STYLE_FILE = os.path.abspath(STYLE_FILE)
    ANNOTATIONS_FILE = os.path.abspath(ANNOTATIONS_FILE)
    print("---absolute output path: ", OUTPUT_FILE)
    print("---absolute style path: ", STYLE_FILE)
    print("---absolute annotations path: ", ANNOTATIONS_FILE)
    
    #* Gather data used to generate node anotations
    # Use the version with the header line
    pepMapFile = os.path.join(tps_in_dir, 'peptide-mapping.tsv')
    pepFirstFile = os.path.join(tps_in_dir, 'p-values-first.tsv')
    pepPrevFile = os.path.join(tps_in_dir, 'p-values-prev.tsv')
    print(pepMapFile)
    print(pepFirstFile)
    print(pepPrevFile)


    # Use the version for which log2 fold change has been precomputed
    timeSeriesFile = os.path.join(baseDir,'data', 'timeseries', 'log2FoldChange011215.txt')
    #timeSeriesFile = r"C:\\Users\\ajshe\\Anaconda3\\envs\\py2cyto\\tps\\data\\timeseries\\log2FoldChange011215.txt"
    print(timeSeriesFile)

    windowsFile = os.path.join(baseDir,'workflow','activity-windows.tsv')
    networkFile = os.path.join(baseDir,'workflow', 'output.sif')
    print(windowsFile)
    print(networkFile)

    # Use the same EGFR gold standard for Olsen 2006 and Ale's data
    goldStandardFile = os.path.join(baseDir, 'data', 'resources', 'eight-egfr-reference-all.txt')

    styleTemplateFile = os.path.join(baseDir,'notebooks', 'tps_style_template.xml')

    out_dir = os.path.join(baseDir, 'results', str(today) + '-and-wolf-yadlin-TPS-cytoscape')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print('Created {}'.format(out_dir))
    outFile = os.path.join(out_dir, 'wolf-yadlin-cytoscape-annotations-'+ str(today) + '.txt')
    outStyleFile = os.path.join(out_dir, 'tps_style.xml')

    #* run Utility function
    pvalThresh = 0.01  # Same threhsold used in TPS
    logTransform = False
    pepsPerProt = PrepTemporalCytoscapeTPS(pepMapFile, timeSeriesFile, pepFirstFile,
                                                pepPrevFile, windowsFile, networkFile,
                                                goldStandardFile, pvalThresh, logTransform, styleTemplateFile,
                                                outFile,
                                                outStyleFile,
                                                addZero=True)  # don't provide logDefault
    
    #* get annotations file 
    ANNOTATIONS_FILE = outFile
   
    
    #* Prepare data and directories


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
    switch = False
    start = time.time()
    while switch is False:
        try:

            # run visualization function 
            vis(OUTPUT_FILE, STYLE_FILE, ANNOTATIONS_FILE)

            # print information --------------------------------
            print("---CyRest client created")
            print("---output file: " + OUTPUT_FILE)
            print("---style file: " + STYLE_FILE)
            print("---ConnectionError catches: ", connection_count)
            print("---JSONDecoderError catches: ", JSON_count)
            # --------------------------------------------------

            # flip switch value
            switch = True

        except CE as e:
            
            #requests.ConnectionError caught if connection cannot be made with Cytoscape Server
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
    end = time.time()
    print("---time elapsed: ", end - start)  

    print("---Finish loading output file and style file")
  


if __name__ == '__main__':
    main(sys.argv)