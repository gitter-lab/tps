import os
import subprocess
import pytest
from workflow import ConfigParser

CONFIGS = {
    'default': 'default.yaml',
    'tps-no-container': 'tps-no-container.yaml'
}
class TestWorkFlow:

    @classmethod
    def setup_method(self):
        self.tps_root = os.getcwd()
        self.tps_main = os.path.join(self.tps_root, 'tps_workflow.py')

    @pytest.mark.parametrize('config_type', ['default', 'tps-no-container'])
    def test_tps_workflow(self, config_type):
        config = os.path.join(self.tps_root, 'workflow', 'tests', 'standards', CONFIGS[config_type])
        # with open(config, 'r') as conf:
        #     settings = ConfigParser.parse(config)
        call = ['python', self.tps_main, 
                '--config', config, '--execute', 'tps']
        assert subprocess.run(call, check=True).returncode == 0

        outputs = [
                os.path.join(self.tps_root, 'test-output', 'test-runner-full-temporal-interpretation.tsv'),
                os.path.join(self.tps_root, 'test-output', 'test-runner-full-activity-windows.tsv'),
                os.path.join(self.tps_root, 'test-output', 'test-runner-full-output.sif'),
                os.path.join(self.tps_root, 'test-output', 'test-runner-full-output.tsv')
        ]
            
        for file in outputs:
            assert os.path.isfile(file)
            os.remove(file)

    @pytest.mark.parametrize('config_type', ['default', 'tps-no-container'])
    def test_annotations(self, config_type):
        config = os.path.join(self.tps_root, 'workflow', 'tests', 'standards', CONFIGS[config_type])
        # with open(config, 'r') as conf:
        #     settings = ConfigParser.parse(config)
        call = ['python', self.tps_main, 
                '--config', config, '--execute', 'annotations']
        
        assert subprocess.run(call, check=True).returncode == 0

        outputs = [
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-temporal-interpretation.tsv'),
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-activity-windows.tsv'),
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-output.sif'),
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-output.tsv'),
            os.path.join(self.tps_root, 'test-output', 'style_output.xml'),
            os.path.join(self.tps_root, 'test-output', 'test-annot-full.txt')
        ]

        for file in outputs:
            assert os.path.isfile(file)
            os.remove(file)

    @pytest.mark.parametrize('config_type', ['default', 'tps-no-container'])
    def test_full(self, config_type):
        config = os.path.join(self.tps_root,'workflow', 'tests', 'standards', CONFIGS[config_type])
        # with open(config, 'r') as conf:
        #     settings = ConfigParser.parse(config)
        call = ['python', self.tps_main, 
                '--config', config, '--execute', 'all']
        
        assert subprocess.run(call, check=True).returncode == 0

        outputs = [
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-temporal-interpretation.tsv'),
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-activity-windows.tsv'),
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-output.sif'),
            os.path.join(self.tps_root, 'test-output', 'test-runner-full-output.tsv'),
            os.path.join(self.tps_root, 'test-output', 'style_output.xml'),
            os.path.join(self.tps_root, 'test-output', 'test-annot-full.txt'),
            os.path.join(self.tps_root, 'test-output', 'tps_session_full.cys'),
            os.path.join(self.tps_root, 'test-output', 'tps_session_full.pdf')
        ]

        for file in outputs:
            assert os.path.isfile(file)
            os.remove(file)
