import yaml
import pprint
import sys
import subprocess
import os

def parse(config):

    '''
    parse input config file 

    build TPS call 

    store output dir 
    '''

    args = ['--network', \
    '--timeseries', \
    '--firstscores', \
    '--prevscores', \
    '--partialmodel', \
    '--peptidemap', \
    '--source',    \
    '--threshold'] 

    with open(config) as c:
        params = yaml.load(config)

    tps_paramS = []

    # grab TPS params 
    build = []
    for key, val in params[1]["TPS"].items():
        k = "--" + key
        build.append(k + " " + str(val))
    
    build   



def main(args):

    CONFIG = args[0]
    parse(CONFIG)





if __name__ == "__main__":
    main(sys.argv)

