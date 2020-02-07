""" 
script loads style file and TPS output file into Cytoscape session

@author: Adam Shedivy

"""

# imports 
from py2cytoscape.data.cynetwork import CyNetwork
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape.data.style import StyleUtil
import py2cytoscape.util.cytoscapejs as cyjs
import py2cytoscape.cytoscapejs as renderer

import networkx as nx
import pandas as pd
import json
import sys

# client used for vizmap functions 
# edit made in table.py:
# "C:\Users\ajshe\AppData\Roaming\Python\Python35\site-packages\py2cytoscape\cyrest\table.py", line 575
# changed else to finally 1/24/2020
from py2cytoscape import cyrest

def main(args):
    """
    REQUIRED ARGS:
        NETORK OUTPUT FILE: output file from tps software
        STYLE FILE: style file for cytoscpe 
    """

    OUTPUT_FILE = args[1]
    STYLE_FILE = args[2]
    print("output file: " + OUTPUT_FILE)
    print("style file: " + STYLE_FILE)

    #create cyrest client
    cyy = cyrest.cyclient()
    print("CyRest client created")

    # Step 1: Create py2cytoscape client
    cy = CyRestClient()

    # Reset
    cy.session.delete()
    print("session reset")

    # Step 2: Load network from somewhere
    print("loading network file")
    tps_net = cy.network.create_from(OUTPUT_FILE)
    print("Done")


    # Step 3: Apply layout
    # list of styles to apply
    # only contains the one style loaded from style file 
    print("apply style file")
    style = cyy.vizmap.load_file(STYLE_FILE)
    print("style name: ", style)
    cyy.vizmap.apply(style[0])

    print("Done! open up cytoscape session")

if __name__ == '__main__':
    main(sys.argv)












