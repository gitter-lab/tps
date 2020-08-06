'''
tests for data refactoring of annotations and style files 

@author Adam Shedivy 2020-07-29

'''

import os
import pandas as pd


def test_table_refactor(new_annotatations):
    '''
    test refactoring code used for annotations data
    
    :param new_annotations - new generated file from workflow
    
    '''
    
    # get test standard
    test_base = os.path.dirname(os.path.abspath(__file__))
    orig_annotations = os.path.join(test_base, 'test_standards', 'wolf-yadlin-cytoscape-annotations-original.txt')
    
    # get recent workflow output
    tps = os.path.abspath(os.path.join('..'))
    results = os.path.join(tps, 'results', '2020-06-30-and-wolf-yaldin-TPS-cytoscape', 'wolf-yadlin-cytoscape-annotations-2020-06-30.txt')
    
    # load data into dataframes
    orig_df = pd.read_csv(orig_annotations, delimiter='\t')
    results_df = pd.read_csv(orig_annotations, delimiter='\t')
    
    check = orig_df.equals(results_df)
    
    if check is False:
        print("dataframes not equal")
        return False
    else:
        return True
    
    return False
    
    

def main():

    val = test_table_refactor(None)
    if val is True:
        print('test passed')
    else:
        print('test failed')
    print('test ended')
    
if __name__ == "__main__":
    main()