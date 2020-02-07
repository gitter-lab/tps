#######################################################
# find Cytoscape application on user's machine 
# returns Path to Cytoscape
#######################################################
import os
import sys

#TODO use directory closer to top
#! use more efficient search algorithm

dirname = r"C:\Users\ajshe\OneDrive\Documents\Comp_bio\Cytoscape_v3.7.1"
#dirname = r"C:\Users"

def find_path(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result[0]

def main():
    print(find_path('Cytoscape.exe', dirname))
    sys.exit(0)

if __name__ == "__main__":
    main()

