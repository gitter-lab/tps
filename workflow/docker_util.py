import docker
import re
import functools
from pathlib import PurePath, Path
from typing import Dict, Optional, Any

from workflow.runner import *


CLIENTS = {
    'TPS'       : 'ajshedivy/tps',
    'CYTOSCAPE' : 'ajshedivy/cytoscape'
}

SEP = '/'

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

    def prepare_tps(self) -> Dict[str, Any]:
        """Helper function for preparing TPS Container Settings

        Returns:
            Dict[str, Any]: collection of Docker Settings
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

        Returns:
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
        container_settings['command']  = self.build_cytoscape_command()
        container_settings['volumes']  = {
            output_path : {'bind': '/cytoscape/'+self.workflow_runner.out_folder, 'mode': 'rw'}
        }

        container_settings['ports'] = {
            '1234' : 1234,
            '5900' : 5900
        }

        container_settings['container_wdir'] = '/cytoscape'
        return container_settings

    def build_cytoscape_command(self):
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

        container_settings = self.DOCKER_SETTINGS.get(
            self.client_name, lambda: f'invalid client: {self.client}')()

        # Initialize a Docker client using environment variables
        client = docker.from_env()

        try:
            container_output = client.containers.run(
                self.client,
                container_settings['command'],
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
