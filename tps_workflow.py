'''
The TPS Workflow is an encapsulated python-centric wrapper for the TPS core 
software. The TPS input settings are defined in a config file that is 
passed into the /workflow.sh driver script to start the workflow run.
Once complete, all tps output files are placed in the specified output directory

usage: bash workflow.sh --config [config.yml] --execute [all|annotations|tps]

To run full workflow : 
    bash workflow.sh --config workflow/config/config.yaml --execute all

@author : Adam Shedivy

'''

import yaml
import argparse
import workflow
from typing import Dict, Any
from workflow.workflow import Runner, Annotations, Visualize

yaml.warnings({'YAMLLoadWarning': False})


def get_parser() -> argparse.ArgumentParser:
    '''
    :return: an argparse ArgumentParser object for parsing command
        line parameters
    '''
    parser = argparse.ArgumentParser(
        description='Run TPS pipeline.')

    parser.add_argument('--config', default='config.yaml',
        help='Path to config file')
    parser.add_argument('--execute', 
        default='all',
        choices=['all', 'tps', 'annotations'],
        help='choose steps of workflow to execute')

    return parser

def parse_arguments() -> Dict[str, Any]:
    '''
    Initialize a parser and use it to parse the command line arguments
    :return: parsed dictionary of command line arguments
    '''
    parser = get_parser()
    opts = parser.parse_args()

    return opts


def main():
    opts = parse_arguments()
    config_file = opts.config
    rule = opts.execute

    with open(config_file, 'r') as conf:
        params = workflow.ConfigParser.parse(conf)

    if rule.lower() == 'all':

        runner = Runner(params).run_tps()
        annotations = Annotations(
            params.annot_input_settings,
            runner
        ).generate_annotations()

        Visualize(
            params.cytoscape_input_settings,
            runner,
            annotations
        ).load_cytoscape()

    elif rule == 'annotations':

        runner = Runner(params).run_tps()
        annotations = Annotations(
            params.annot_input_settings,
            runner
        ).generate_annotations()

    elif rule == 'tps':

        runner = Runner(params).run_tps()

    else:
        print(f'rule {rule} not specified')

    print('Evaluation complete')

if __name__ == '__main__':
    main()
