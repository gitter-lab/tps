'''
Design inspired by 
https://github.com/Murali-group/Beeline/blob/master/BLRun/__init__.py

'''
from calendar import c
import yaml
import os
from typing import Dict, Any, Union
from pathlib import Path
import sys

# define defaults to be used during initialization
TPS_ROOT                    =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_FOLDER       = os.path.join(TPS_ROOT, 'output')
DEFAULT                     = '<value-here>'
OUTPUT_FOLDER               = 'outfolder'
TPS_RUN                     = './scripts/run'
CYTOSCAPE_DATATYPES         = ""  # data type list set in runner.Annotations.generate_annotations

class CytoscapeSettings(object):
    '''
    wrapper object for cytoscape settings defined in config file

    '''
    def __init__(self, path, session, name):
        self.path    = path
        self.session = session
        self.name    = name

        

class TPSSettings(object):
    '''
    wrapper object for TPS settings defined in config file

    '''
    def __init__(self, required: Dict[str, Any], optional, flags):
        self.required     = required
        self.optional     = optional
        self.flags        = flags
        self.output_label = required['outlabel']
        self.args         = self.__parse_input_settings()

    def __parse_input_settings(self) -> Dict[str, Any]:
        filtered_ags = {**self.required, 
                    **self.optional}
        args = {key:val for key, val in filtered_ags.items()
                    if filtered_ags[key] != 'None'}
        return args

    def _add_setting(self, key:str, val: Union[str, Path]):
        if key in self.args:
            raise KeyError(f'key: {key} already provided')
        self.args[key] = val      


class AnnotationsSettings(object):
    '''
    wrapper object for annotations settings defined in config file

    '''
    def __init__(self, annotations):
        self.annotations = annotations

    def __getitem__(self, key):
        return self.annotations[key]

class DockerSettings(object):
    def __init__(self, settings: Dict[str, Any]):
        self.docker_settings = settings
        self.use_tps      = self.docker_settings['TPS']
        self.use_cytoscape   = self.docker_settings['Cytoscape']
        


class WorkflowRun(object):
    '''
    the WorkflowRun object is created by parsing a user-definded configuration
    file. Its methods are used to structure the inputs in an object oriented way as 
    well as build a TPS run configuration

    '''

    def __init__(self,
                cytoscape_input_settings: CytoscapeSettings,
                tps_input_settings: TPSSettings,
                annot_input_settings: AnnotationsSettings,
                docker_settings: DockerSettings,
                config_file: Union[str, Path]):
        self.config_file              = config_file
        self.cytoscape_input_settings = cytoscape_input_settings
        self.tps_input_settings       = tps_input_settings
        self.annot_input_settings     = annot_input_settings
        self.docker_settings          = docker_settings
        self.out_folder               = self.__get_out_folder()
        self.build                    = self.__build_tps_inputs(tps_input_settings)
        
        


    def __build_tps_inputs(self, tps_input_settings):
        build = ['bash', TPS_RUN]
        for key, val in self.tps_input_settings.args.items():
            k = '--' + key
            build.extend([k, str(val)])
        if tps_input_settings.flags is not None:
            build.extend(tps_input_settings.flags)
        return build

    def __make_out_folder(self, folder: Union[str, Path]) -> None:
        if not os.path.exists(folder):
            os.makedirs(folder)

    def __get_out_folder(self) -> None:
        """
        if output folder provided in config:
            return folder
        if not using tps container but executing annot or all:
            use default output folder in repo
        else
            return tps root 


        Returns:
            Union[Path, str]: output folder
        """
        out_folder = None
        if OUTPUT_FOLDER in self.tps_input_settings.args:
            print(f'outfolder provided: {self.tps_input_settings.args[OUTPUT_FOLDER]}')
            out_folder = self.tps_input_settings.args[OUTPUT_FOLDER]
            self.__make_out_folder(out_folder)
        else:
            print("Error: provide output folder in {self.config_file.name} and re-run workflow")
            print("exiting script")
            sys.exit()

        return out_folder

class ConfigParser(object):
    '''
    define static methods to be used for parsing the config file 
    
    '''

    @staticmethod
    def parse(config_file_handle: Union[str, Path]) -> WorkflowRun:
        config_map = yaml.safe_load(config_file_handle)
        return WorkflowRun(
            ConfigParser.__parse_cytoscape_settings(
                config_map['Cytoscape']),
            ConfigParser.__parse_tps_settings(
                config_map['TPS']),
            ConfigParser.__parse_annotations_settings(
                config_map['Annotations']),
            ConfigParser.__parse_docker_settings(
                config_map['Docker']
            ),
            config_file_handle
        )

    @staticmethod
    def __parse_cytoscape_settings(cytoscape_settings_map) -> CytoscapeSettings:
        return CytoscapeSettings(cytoscape_settings_map['path'],
                        cytoscape_settings_map['session'], 
                        cytoscape_settings_map['name'])

    @staticmethod
    def __parse_tps_settings(tps_settings_map) -> TPSSettings:
        required = tps_settings_map['required']
        optional = tps_settings_map.get('optional', [])
        flags    = tps_settings_map.get('flags', [])

        return TPSSettings(required, optional, flags)

    @staticmethod
    def __parse_annotations_settings(annot_settings_map) -> AnnotationsSettings:
        return AnnotationsSettings(annot_settings_map)

    @staticmethod
    def __parse_docker_settings(docker_settings) -> DockerSettings:
        return DockerSettings(docker_settings)
