import os
import subprocess
import pytest

CONFIGS = {
    'default':'default.yaml',
    'tps-cytoscape':'tps-cytoscape.yaml',  # does not exist yet
    'tps-no-container':'tps-no-container.yaml'
}
class TestWorkFlow:

    @classmethod
    def setup_method(self):
        self.tps_root = os.getcwd()
        self.tps_main = os.path.join(self.tps_root, 'tps_runner.py')

    @pytest.mark.parametrize('config_type', ['default', 'tps-no-container'])
    def test_tps_workflow(self, config_type):
        config = os.path.join(self.tps_root,'workflow' ,'tests', 'standards', CONFIGS[config_type])
        call = ['python', self.tps_main, 
                '--config', config, '--execute', 'tps']
        assert subprocess.run(call, check=True).returncode == 0

        outputs = [
            os.path.join(self.tps_root, 'output', 'test-runner-full-temporal-interpretation.tsv'),
            os.path.join(self.tps_root, 'output', 'test-runner-full-activity-windows.tsv'),
            os.path.join(self.tps_root, 'output', 'test-runner-full-output.sif'),
            os.path.join(self.tps_root, 'output', 'test-runner-full-output.tsv')
        ]
        for file in outputs:
            assert os.path.isfile(file)  

    # def test_cytoscape():
    #     ...

    # def test_full():
    #     ...

    # def test_tps_container():
    #     ...

    # def test_cytoscape_container():
    #     ...
