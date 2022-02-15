import docker
import os
import sys
import pandas as pd
import warnings
from pathlib import Path, PurePath
from docker_util import prepare_path_docker


def run():
    command = ['bash', './scripts/run', '--network', 
    'data/networks/input-network.tsv', '--timeseries', 
    'data/timeseries/median-time-series.tsv', '--firstscores', 
    'data/timeseries/p-values-first.tsv', '--prevscores', 
    'data/timeseries/p-values-prev.tsv', '--source', 'EGF_HUMAN', 
    '--threshold', '0.01', '--outlabel', 'test-runner-full', '--partialmodel', 
    'data/resources/kinase-substrate-interactions.sif', 
    '--peptidemap', 'data/timeseries/peptide-mapping.tsv']



    # TODO: fix docker call for tps
    try:
            uid = os.getuid()
    except AttributeError:
            need_chown = False

    try:
        container_output = client.containers.run(
            'reedcompbio/pathlinker',
            command,
            stderr=True,
            volumes={
                prepare_path_docker(work_dir): {'bind': '/home/spras', 'mode': 'rw'}
            },
            working_dir='/home/spras/')
        print(container_output.decode('utf-8'))
        if need_chown:
            #This command changes the ownership of output files so we don't
            # get a permissions error when snakemake tries to touch the files
            # PathLinker writes output files to the working directory
            chown_command = " ".join(['chown',str(uid),'./out*-ranked-edges.txt'])
            client.containers.run('reedcompbio/pathlinker',
                                    chown_command,
                                    stderr=True,
                                    volumes={prepare_path_docker(work_dir): {'bind': '/home/spras', 'mode': 'rw'}},
                                    working_dir='/home/spras/')

    finally:
        # Not sure whether this is needed
        client.close()
