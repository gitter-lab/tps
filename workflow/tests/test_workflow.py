import os 
import subprocess


class TestWorkflow:

    @classmethod
    def setup_method(self):
        self.tps_root = os.getcwd()
        self.config = os.path.join(
            self.tps_root, 'workflow', 'tests', 'test_standards', 'test_default_config.yaml'
        )
        self.tps_runner = os.path.join(self.tps_root, 'tps_runner.py')

    def test_tps(self):
        print(f'tps_root: {self.tps_root}')
        print(f'tps_runner: {self.tps_runner}')
        assert os.path.isfile(self.tps_runner)
        assert os.path.isdir(self.tps_root)
        call = ['python', self.tps_runner, 
                '--config', self.config, '--execute', 'tps']
        assert subprocess.run(call, check=True).returncode == 0

        outputs = [
            os.path.join(self.tps_root, 'test-runner-full-temporal-interpretation.tsv'),
            os.path.join(self.tps_root, 'test-runner-full-activity-windows.tsv'),
            os.path.join(self.tps_root, 'test-runner-full-output.sif'),
            os.path.join(self.tps_root, 'test-runner-full-output.tsv')
        ]
        for file in outputs:
            assert os.path.isfile(file)

    def test_annotations(self):
        call = [
            'python', self.tps_runner, 
            '--config', self.config, '--execute', 'annotations'
        ]
        assert subprocess.run(call, check=True).returncode == 0
        outputs = [
            os.path.join(self.tps_root, 'test-annot-full.txt'),
            os.path.join(self.tps_root, 'style_output.xml')
        ]
        for file in outputs:
            assert os.path.isfile(file)

    def test_cytoscape_session(self):
        pass



