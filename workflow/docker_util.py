'''
This file defines the utility functions and classes used for interation
with Docker

@author : Adam Shedivy

'''

import functools
import re
from pathlib import Path, PurePath
from typing import Any, Dict, List, Optional

import docker

from workflow.workflow import *

CLIENTS = {
    'TPS'       : 'ajshedivy/tps',
    'CYTOSCAPE' : 'ajshedivy/cytoscape'
}

SEP = '/'
RUNNING = 'running'

def prepare_path_docker(orig_path: PurePath) -> str:
    """
    Prepare an absolute path for mounting as a Docker volume.
    Converts Windows file separators to posix separators.
    Converts Windows drive letters in absolute paths.

    Modified from the SPRAS code
    Source: https://github.com/Reed-CompBio/spras
    Available under the MIT license
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


def is_container_running(container_name: str) -> bool:
    """check if a container is running

    Parameters
    ----------
    container_name : str
        name of container assigned after calling docker run

    Returns
    -------
    bool
        True if running, else False
    """

    client = docker.from_env()
    
    # test if current Container (TPS or Cytoscape) is running
    try:
        container = client.containers.get(container_name)

    # the current container is not running (cant be found) -> False
    except docker.errors.NotFound as ex:
        return False

    # APIErrors can happen
    except docker.errors.APIError as ex:
        print(f"{ex.explanation}")
        client.close()
        sys.exit()
          
    # check container status here, means that current container is probably running
    else:
        container_state = container.attrs["State"]
        return container_state["Status"] == RUNNING



class DockerClient(object):
    """
    A class used to prepare docker containers for TPS workflow. Used by workflow/workflow.py

    ...

    Attributes
    ----------
    client_name : str
        string name of container to prepare
    client : str
        name of container tag
    worflow_runner : Optional[WorkflowRun]
        workflow object with input parameters and settings
    outfolder : Union[str, Pathlike]
        ouput folder location
    cytoscape : Optional[Visualize]
        cytoscape input and parameter settings

    Methods
    -------
    prepare_tps(self) -> Dict[str, Any]
        prepare TPS docker input settings

    prepare_cytoscape(self) -> Dict[str, Any]
        prepare Cytoscape docker input settings

    _build_cytoscape_command(self) -> List[str]
        helper function for generating cytoscape bash run command

    run_docker(self) -> None
        run specified docker client

    """
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

    def prepare_tps(self) -> Dict[str, Any]:
        """helper function for generating tps docker input settings. Used when client_name = 'TPS'

        Returns
        -------
        Dict[str, Any]
            dictionary of docker input settings used by run_docker
        """
        container_settings = {
            'work_dir':None,
            'command':None,
            'volumes': Dict[str, Dict[str, Any]],
            'container_wdir':None,
        }

        work_dir    = Path(__file__).parent.parent.absolute()
        data_path   = prepare_path_docker(work_dir)+'/data'
        output_path = prepare_path_docker(work_dir)+SEP+self.workflow_runner.out_folder
        
        container_settings['work_dir'] = work_dir
        container_settings['command']  = self.workflow_runner.build
        container_settings['volumes']  = {
            data_path : {'bind': '/tps/data', 'mode': 'rw'},
            output_path : {'bind': '/tps/'+self.workflow_runner.out_folder, 'mode': 'rw'}
        }
        container_settings['container_wdir'] = '/tps'
        container_settings['ports'] = {}

        return container_settings


    def prepare_cytoscape(self) -> Dict[str, Any]:
        """helper for preparing cytoscape container settings

        requirements:
            - output directory
            - style file
            - annotations file
            - network file
        Returns
        -------
        Dict[str, Any]
            Dict[str, Any]: collection of Docker Settings
        """
        container_settings = {
            'work_dir':None,
            'command':None,
            'volumes': Dict[str, Dict[str, Any]],
            'ports': Dict[str, Dict[str, Any]],
            'container_wdir':None,
        }

        work_dir    = Path(__file__).parent.parent.absolute()
        output_path = prepare_path_docker(work_dir)+'/'+self.workflow_runner.out_folder

        container_settings['work_dir'] = work_dir
        container_settings['command']  = self._build_cytoscape_command()
        container_settings['volumes']  = {
            output_path : {'bind': '/cytoscape/'+self.workflow_runner.out_folder, 'mode': 'rw'}
        }

        container_settings['ports'] = {
            '1234' : 1234,
            '5900' : 5900
        }

        container_settings['container_wdir'] = '/cytoscape'
        return container_settings

    def _build_cytoscape_command(self) -> List[str]:
        """private helper function for build cytoscape run command used in Cytoscape Docker container

        Returns
        -------
        List[str]
            list of bash args
        """
        command = ['bash', 'connect.sh']
        args = {
            '--save':    self.workflow_runner.out_folder + SEP + os.path.basename(self.cytoscape.save_file),
            '--style':   self.workflow_runner.out_folder + SEP + os.path.basename(self.cytoscape.style_file),
            '--annot':   self.workflow_runner.out_folder + SEP + os.path.basename(self.cytoscape.annot_file),
            '--network': self.workflow_runner.out_folder + SEP + os.path.basename(self.cytoscape.network_file),
            '--datatypes': self.cytoscape.data_types
        }
        command.extend(list(functools.reduce(lambda x, y: x+y, args.items())))
        return command

    def run_docker(self) -> None:
        """driver function for running specified docker client"""

        if is_container_running(self.client_name):
            print(f"container: {self.client} is running, please stop container and run workflow again")
            sys.exit()

        container_settings = self.DOCKER_SETTINGS.get(
            self.client_name, lambda: f'invalid client: {self.client}')()

        # Initialize a Docker client using environment variables
        client = docker.from_env()

        try:
            container_output = client.containers.run(
                self.client,
                container_settings['command'],
                remove=True,
                name=self.client_name,
                stderr=True,
                stdout=True,
                volumes=container_settings['volumes'],
                ports=container_settings['ports'],
                working_dir=container_settings['container_wdir'],
                detach=True)
            output = container_output.attach(stdout=True, stream=True, logs=True)
            for line in output:
                print(line.decode('utf-8'))

        finally:
            # Not sure whether this is needed
            client.close()
