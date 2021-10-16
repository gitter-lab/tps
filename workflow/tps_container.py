import docker
import os
import sys
import pandas as pd
import warnings
from pathlib import Path, PurePath


def prepare_path_docker(orig_path: PurePath) -> str:
    """
    Prepare an absolute path for mounting as a Docker volume.
    Converts Windows file separators to posix separators.
    Converts Windows drive letters in absolute paths.
    """
    # TODO consider testing PurePath.is_absolute()
    prepared_path = orig_path.as_posix()
    # Check whether the path matches an absolute Windows path with a drive letter
    match = re.match(r'^([A-Z]:)(.*)', prepared_path)
    if match:
        # The first group is the drive such as C:
        drive = match.group(1).lower()[0]
        # The second group is the rest of the path such as /Users/me
        prepared_path = match.group(2)
        prepared_path = '//' + drive + prepared_path
    return prepared_path



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