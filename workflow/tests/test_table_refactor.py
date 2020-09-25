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
        print(test_base)
        orig_annotations = os.path.join(test_base, 'test_standards', 'wolf-yadlin-cytoscape-annotations-original.txt')

        # get recent workflow output
        tps = os.path.abspath(os.path.join('..'))
        print(tps)
        results = os.path.join(tps, 'tps', 'results', '2020-06-30-and-wolf-yadlin-TPS-cytoscape', 'wolf-yadlin-cytoscape-annotations-2020-06-30.txt')
        
        # load data into dataframes
        orig_df = pd.read_csv(orig_annotations, delimiter='\t')
        edit_df = orig_df.drop(['ActivitySummary2min',	'ActivitySummary4min',	'ActivitySummary8min',	'ActivitySummary16min',	'ActivitySummary32min',	\
            'ActivitySummary64min',	'ActivitySummary128min', 'FirstActive',	'HeatMapBg1',	\
                'HeatMapBg2', 'HeatMapBg3',	'HeatMapBg4',	'HeatMapBg5',	'HeatMapBg6'], axis=1)

        results_df = pd.read_csv(results, delimiter='\t').drop('Unnamed: 19', 1)
        
        assert edit_df.equals(results_df), "dataframes not equal"