import sys
import os
import glob
from multiprocessing import Process

def find_path1(name="Cytoscape.exe", path=r"C:\Users\ajshe\OneDrive\Documents"):
    """
    Search Algorithm to find Cytoscape application on machine

    Args:
        name (str): name of application 
        path (str): top directory to start search from 

    Returns:
        path to first match on machine
    """
    print ("in find_path1")
    # list to hold found matches
    result = []

    # walk directory/file tree 
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    print (result)
    return True

def find_path2(name="Cytoscape.exe", path=r"C:\Users\ajshe\OneDrive"):
    """
    Search Algorithm to find Cytoscape application on machine

    Args:
        name (str): name of application 
        path (str): top directory to start search from 

    Returns:
        path to first match on machine
    """
    print ("in find_path2")
    # list to hold found matches
    result = []

    # walk directory/file tree 
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    print (result)        
    return True

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
    return result

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)

    for p in proc:
        p.join()

def search(init_path):
    next_path = r"C:\Users\ajshe\OneDrive\Documents"
    cyto = find_path('Cytoscape.exe', init_path)
    print ("cyto: ", cyto)
    if not cyto:
        #run new search
        print ("cyto not found in ", init_path)
        cyto2 = find_path('Cytoscape.exe', next_path)
        if len(cyto2) == 1:
            print ("cyto found in higher dir")
            return cyto2[0]
        else:
            print (cyto)
            return
    else:
      return cyto[0]
    
def f1():
    print('function 1 starting')
    for i in range(100):
        pass
    print ("function 1 ending")

def f2():
    print("Function 2 starting")
    for i in range(100):
        pass
    print("function 2 ending")

def main():
   # path = find_path("Cytoscape.exe", r"C:\\") 
   # print(path);
    # p1 = Process(target=find_path2)
    # p1.start()
    # p2 = Process(target=find_path1)
    # p2.start()
    # p1.join()
    # p2.join()

    #find_path('Cytoscape.exe', r"C:\Users\ajshe\OneDrive\Documsdf" )
    search(r"C:\Users\ajshe\OneDrive\Docufff")


if __name__ == '__main__':
    main()
