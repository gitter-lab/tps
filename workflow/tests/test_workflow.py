import os 
import sys
import subprocess
import pytest
from pathlib import Path


class TestWorkflow:

    @classmethod
    def setup_method(self):
        print("setup")
        self.test_base = Path(os.getcwd())
        self.tps_root = self.test_base.parent.parent
        self.config = os.path.join(self.test_base, 'test_standards', 'test_default_config.yaml')
        os.chdir(self.tps_root)

    @classmethod
    def teardown_method(self):
        print("teardown")
        os.chdir(self.test_base)

    def test_tps(self):
        call = ['python', 'tps_runner.py', 
                '--config', self.config, '--execute', 'tps']
        assert subprocess.run(call, check=True).returncode == 0

    def test_annotations(self):
        call = [
            'python', 'tps_runner.py', 
            '--config', self.config, '--execute', 'annotations'
        ]
        assert subprocess.run(call, check=True).returncode == 0

    def test_cytoscape_session(self):
        pass

