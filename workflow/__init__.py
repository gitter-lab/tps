'''
Design inspired by 
https://github.com/Murali-group/Beeline/blob/master/BLRun/__init__.py

'''
import yaml
import os

# define defaults to be used during initialization
DEFAULT_OUT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = '<value-here>'

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
    wrapper object for TPS settings defined in config file

    '''
    def __init__(self, required, optional, flags):
        self.required = required
        self.optional = optional
        self.flags = flags
        self.output_label = required['outlabel']
        self.args = self.__parse_input_settings()

    def __parse_input_settings(self):
        filtered_ags = {**self.required, 
                    **self.optional}
        args = {key:val for key, val in filtered_ags.items()
                    if filtered_ags[key] != 'None'}
        return args


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
    well as build a TPS run configuration

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
        build = ['bash', './scripts/run']
        for key, val in self.tps_input_settings.args.items():
            k = '--' + key
            build.extend([k, str(val)])
        if tps_input_settings.flags is not None:
            build.extend(tps_input_settings.flags)
        return build

    def __get_out_folder(self):
        check = 'outfolder'
        if check in self.tps_input_settings.args:
            print(f'outfolder provided: {self.tps_input_settings.args[check]}')
            out_folder = self.tps_input_settings.args[check]
        else:
            out_folder = DEFAULT_OUT_FOLDER
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
        optional = tps_settings_map.get('optional', [])
        flags = tps_settings_map.get('flags', [])

        return TPSSettings(required, optional, flags)

    @staticmethod
    def __parse_annotations_settings(annot_settings_map):
        return AnnotationsSettings(annot_settings_map)
