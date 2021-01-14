import yaml
import os
from typing import Dict, List

# define defaults to be used during initialization
OUT_LABEL = ""
OUT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(OUT_FOLDER)
DEFAULT = "<value-here>"

class CytoscapeSettings(object):
    '''
    wrapper object for cytoscape settings defined in config file

    '''
    def __init__(self, path, session, name):
        self.path = path
        self.session = session
        self.name = name

        

class TPSSettings(object):
    '''
    wrapper object for TPS settings definded in config file

    '''
    def __init__(self, required, optional, flags):
        self.required = required
        self.optional = optional
        self.flags = flags
        self.output_label = required['outlabel']

class AnnotationsSettings(object):
    '''
    wrapper object for annotations settings defined in config file

    '''
    def __init__(self, annotations):
        self.annotations = annotations

    def __getitem__(self, key):
        return self.annotations[key]

class WorkflowRun(object):
    '''
    the WorkflowRun object is created by parsing a user-definded configuration
    file. Its methods are used to structure the inputs in an object oriented way as 
    well as build a tps run configuration

    '''

    def __init__(self,
                cytoscape_input_settings: CytoscapeSettings,
                tps_input_settings: TPSSettings,
                annot_input_settings: AnnotationsSettings):
        
        self.cytoscape_input_settings = cytoscape_input_settings
        self.tps_input_settings = tps_input_settings
        self.annot_input_settings = annot_input_settings
        self.build = self.__build_tps_inputs(tps_input_settings)
        self.out_folder = self.__get_out_folder()

    def __build_tps_inputs(self, tps_input_settings):
        build = []
        build.extend(["bash", "./scripts/run"])
        filtered_ags = {**tps_input_settings.required, 
                    **tps_input_settings.optional}
        args = {key:val for key, val in filtered_ags.items()
                    if filtered_ags[key] != DEFAULT}

        for key, val in args.items():
            k = "--" + key
            build.extend([k, str(val)])
        if tps_input_settings.flags is not None:
            build.extend(tps_input_settings.flags)

        print(build)
        return build

    def __get_out_folder(self):
        check = 'outfolder'
        if check in self.build:
            out_folder = build[check]
        else:
            out_folder = OUT_FOLDER
        return out_folder


    

class ConfigParser(object):
    '''
    define static methods to be used for parsing the config file 
    
    '''

    @staticmethod
    def parse(config_file_handle) -> WorkflowRun:
        config_map = yaml.load(config_file_handle)
        return WorkflowRun(
            ConfigParser.__parse_cytoscape_settings(
                config_map['Cytoscape']),
            ConfigParser.__parse_tps_settings(
                config_map['TPS']),
            ConfigParser.__parse_annotations_settings(
                config_map['Annotations'])
        )

    @staticmethod
    def __parse_cytoscape_settings(cytoscape_settings_map):
        return CytoscapeSettings(cytoscape_settings_map['path'],
                        cytoscape_settings_map['session'], 
                        cytoscape_settings_map['name'])

    @staticmethod
    def __parse_tps_settings(tps_settings_map):
        required = tps_settings_map['required']
        optional = tps_settings_map['optional']
        flags = tps_settings_map['flags']

        return TPSSettings(required, optional, flags)

    @staticmethod
    def __parse_annotations_settings(annot_settings_map):
        return AnnotationsSettings(annot_settings_map)

    
        