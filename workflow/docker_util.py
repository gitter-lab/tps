import docker
import sys, re, os, shutil, tempfile, hashlib, json, base64, functools
from pathlib import PurePath, Path

from py2cytoscape import data
from workflow import WorkflowRun
from typing import Dict, List, Optional, Any, Type

from workflow.runner import *


CLIENTS = {
    'TPS'       : 'ajshedivy/tps',
    'CYTOSCAPE' : 'ajshedivy/cytoscape'
}


DEFAULT_HASH_LENGTH = 7
DOCKER_OUTFOLDER    = "output/"

def prepare_path_docker(orig_path: PurePath) -> str:
    """
    Prepare an absolute path for mounting as a Docker volume.
    Converts Windows file separators to posix separators.
    Converts Windows drive letters in absolute paths.

    Source: https://github.com/Reed-CompBio/spras
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


def hash_params_sha1_base32(params_dict: Dict[str, Any], length: Optional[int] = None) -> str:
    """
    Hash of a dictionary.
    Derived from https://www.doc.ic.ac.uk/~nuric/coding/how-to-hash-a-dictionary-in-python.html
    by Nuri Cingillioglu
    Adapted to use sha1 instead of MD5 and encode in base32
    Can be truncated to the desired length
    @param params_dict: the algorithm parameters dictionary
    @param length: the length of the returned hash, which is ignored if it is None, < 1, or > the full hash length
    """
    params_hash = hashlib.sha1()
    params_encoded = json.dumps(params_dict, sort_keys=True).encode()
    params_hash.update(params_encoded)
    # base32 includes capital letters and the numbers 2-7
    # https://en.wikipedia.org/wiki/Base32#RFC_4648_Base32_alphabet
    params_base32 = base64.b32encode(params_hash.digest()).decode('ascii')
    if length is None or length < 1 or length > len(params_base32):
        return params_base32
    else:
        return params_base32[:length]

class DockerClient(object):
    def __init__(self, client: str, 
                workflow_settings: Optional[WorkflowRun] = None, 
                cytoscape: Optional[Visualize] = None) -> None:

        self.client_name     = client
        self.client          = CLIENTS[client]
        self.workflow_runner = workflow_settings
        self.outfolder       = workflow_settings.out_folder
        self.cytoscape       = cytoscape
        self.DOCKER_SETTINGS = {
            'TPS'       : self.prepare_tps,
            'CYTOSCAPE'  : self.prepare_cytoscape
        }

    def _collect_files(self) -> List[os.PathLike]:
        self.files_ = []
        for _ , path in self.workflow_runner.tps_input_settings.args.items():

            try:
                temp_file = Path(path)
                if temp_file.is_file():
                    self.files_.append(temp_file)
                else:
                    print(f"{path} not path")
            except TypeError:
                print('not path')

        temp_dir = tempfile.mkdtemp(dir=Path('data'))

    def create_temporary_copy(self, path):
        temp_dir = tempfile.gettempdir()
        print(temp_dir)
        temp_path = os.path.join(temp_dir, 'temp_file_name')
        shutil.copy2(path, temp_path)
        return temp_path

    def _create_output_dir(self) -> None:
        '''
        generate output tag: output_tag_

        '''
        check_build = {
            self.workflow_runner.build[i]: self.workflow_runner.build[i+1] \
            for i in range(0, len(self.workflow_runner.build), 2)
        }

        if '--outfolder' in check_build:
            print('override outfolder location')
            del check_build['--outfolder']
            self.workflow_runner.build = list(functools.reduce(lambda x, y: x+y, check_build.items()))

        self.output_tag_ = DOCKER_OUTFOLDER

        self.workflow_runner.build.extend(['--outfolder', self.output_tag_])
        self.workflow_runner.out_folder = self.output_tag_

    def prepare_tps(self) -> Dict[str, Any]:
        """Helper fucntion for preparing TPS Container Settings

        Returns:
            Dict[str, Any]: collection of Docker Settings
        """
        self._create_output_dir()
        container_settings = {
            'work_dir':None,
            'command':None,
            'volumes': Dict[str, Dict[str, Any]],
            'container_wdir':None,
        }

        work_dir    = Path(__file__).parent.parent.absolute()
        data_path   = prepare_path_docker(work_dir)+'/data'
        output_path = prepare_path_docker(work_dir)+'/'+self.output_tag_
        
        container_settings['work_dir'] = work_dir
        container_settings['command']  = self.workflow_runner.build
        container_settings['volumes']  = {
            data_path : {'bind': '/tps/data', 'mode': 'rw'},
            output_path : {'bind': '/tps/'+self.output_tag_, 'mode': 'rw'}
        }
        container_settings['container_wdir'] = '/tps'

        return container_settings


    def prepare_cytoscape(self) -> Dict[str, Any]:
        """helper for preparing cytoscape container settings

        requirements:
            - output directory
            - 

        Returns:
            Dict[str, Any]: collection of Docker Settings
        """
        pass


    def run(self) -> None:
        self._create_output_dir()

         # Initialize a Docker client using environment variables
        client = docker.from_env()

        # work dir set as the root of the repository
        work_dir = Path(__file__).parent.parent.absolute()

        try:
            container_output = client.containers.run(
                self.client,
                self.workflow_runner.build,
                stderr=True,
                volumes={
                    prepare_path_docker(work_dir)+'/data': {'bind': '/tps/data', 'mode': 'rw'},
                    prepare_path_docker(work_dir)+'/'+self.output_tag_: {'bind': '/tps/'+self.output_tag_, 'mode': 'rw'}
                },
                working_dir='/tps')
            print(container_output.decode('utf-8'))

        finally:
            # Not sure whether this is needed
            client.close()


    def run_docker(self) -> None:

        container_settings = self.DOCKER_SETTINGS.get(
            self.client_name, lambda: f'invalid client: {self.client}')()

         # Initialize a Docker client using environment variables
        client = docker.from_env()

        try:
            container_output = client.containers.run(
                self.client,
                container_settings['command'],
                stderr=True,
                volumes=container_settings['volumes'],
                working_dir=container_settings['container_wdir'])
            print(container_output.decode('utf-8'))

        finally:
            # Not sure whether this is needed
            client.close()




