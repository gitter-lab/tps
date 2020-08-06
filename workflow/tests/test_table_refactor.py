'''
tests for data refactoring of annotations and style files 

@author Adam Shedivy 2020-07-29

'''

import os
import pandas as pd

class TestAnnotations:

    def test_table_refactor(self):
        '''
        test refactoring code used for annotations data
                
        '''
        
        # get test standard
        test_base = os.path.dirname(os.path.abspath(__file__))
        orig_annotations = os.path.join(test_base, 'test_standards', 'wolf-yadlin-cytoscape-annotations-original.txt')
        
        # get recent workflow output
        tps = os.path.abspath(os.path.join('..'))
        results = os.path.join(tps, 'results', '2020-06-30-and-wolf-yaldin-TPS-cytoscape', 'wolf-yadlin-cytoscape-annotations-2020-06-30.txt')
        
        # load data into dataframes
        orig_df = pd.read_csv(orig_annotations, delimiter='\t')
        results_df = pd.read_csv(results, delimiter='\t')
        
        assert orig_df.equals(results_df), "dataframes not equal"
