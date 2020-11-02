""" 
script loads style file and TPS output file into Cytoscape session

@author: Adam Shedivy

"""

# imports
import sys
import time
import subprocess
import os
from requests.exceptions import ConnectionError as CE
from json.decoder import JSONDecodeError
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape import cyrest

# assert Cytoscape is running on machine


def process_exists(process_name):
    """
    function to assert Cytoscape is running

    Args:
        process_name (str): name of process to check for
        example - 'Cytoscape.exe'

    Returns:
        true if process runnning, else false

    """
    bytes_name = str.encode(process_name)
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name

    # use buildin check_output right away
    output = subprocess.check_output(call)

    # check in last line for process name
    last_line = output.strip().split(b'\r\n')[-1]

    return last_line.lower().startswith(bytes_name.lower())


def find_path(name, path):
    """
    Search Algorithm to find Cytoscape application on machine

    Args:
        name (str): name of application 
        path (str): top directory to start search from 

    Returns:
        path to first match on machine
    """

    # list to hold found matches
    result = []

    # walk directory/file tree
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result[0]


def vis(output, style, table, path):
    """
    REQUIRED ARGS:
        output: output file from tps software
        style: style file for cytoscpe 
    """

    # create cyrest client
    cyy = cyrest.cyclient()

    # Step 1: Create py2cytoscape client
    cy = CyRestClient()

    # Reset
    cy.session.delete()
    print("---session reset")

    # Step 2: Load network from somewhere
    print("---loading network file")
    cy.network.create_from(output)
    print("---Done")
    time.sleep(2)

    # Step 3: Apply layout
    # list of styles to apply
    # only contains the one style loaded from style file
    print("---apply style file")
    style = cyy.vizmap.load_file(style)
    print("---style name: ", style)
    cyy.vizmap.apply(style[0])

    # import annotations
    cyy.table.import_file(afile=table,
                          firstRowAsColumnNames=True,
                          keyColumnIndex='1',
                          startLoadRow='0',
                          dataTypeList="s,s,b,dl,dl,dl,dl,dl,dl,dl,dl,dl,dl,dl,dl,dl,dl,dl,dl"
                          )
    
    cyy.session.save_as(session_file=path)

    print("Done! open up cytoscape session")