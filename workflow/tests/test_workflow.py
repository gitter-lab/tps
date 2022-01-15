import os
import subprocess

CONFIGS = {
    'default':'default.yaml',
    'tps-cytoscape':'tps-cytoscape.yaml',
    'tps-no-container':'tps-no-container.yaml'
}
class TestWorkFlow:

    @classmethod
    def setup_method(self):
        self.tps_root = os.getcwd()
        self.tps_main = os.path.join(self.tps_root, 'tps_runner.py')
    
    def test_workflow_default(self):
        config = os.path.join(self.tps_root,'workflow' ,'tests', 'standards', CONFIGS['default'])
        call = ['python', self.tps_main, 
                '--config', config, '--execute', 'tps']
        assert subprocess.run(call, check=True).returncode == 0

    def test_tps_no_container(self):
        config = os.path.join(self.tps_root, 'workflow','tests', 'standards', CONFIGS['tps-no-container'])
        call = ['python', self.tps_main, 
                '--config', config, '--execute', 'tps']
        assert subprocess.run(call, check=True).returncode == 0        

    # def test_cytoscape():
    #     ...

    # def test_full():
    #     ...

    # def test_tps_container():
    #     ...

    # def test_cytoscape_container():
    #     ...