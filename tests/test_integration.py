from unittest import TestCase
import subprocess
import os
import shutil

class TestCompilerRun(TestCase):
    def setUp(self):
        self.test_working_directory = os.path.dirname(os.path.abspath(__file__))
        self.output_directory = os.path.join(self.test_working_directory, 'output')
        self.input_directory = os.path.join(self.test_working_directory, 'input')
        self.compiler_path = os.path.join(self.test_working_directory, '../compiler.py')
        # if the output directory exists, delete it and if it doesn't exist, create it
        if os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)
        os.makedirs(self.output_directory)

    def tearDown(self):
        shutil.rmtree(self.output_directory)

    def test_complete_compiler_run_should_be_successful(self):
        source_file = os.path.join(self.input_directory, 'successful.txt')
        output_file = os.path.join(self.output_directory, 'output_successful.py')
        subprocess.run(["poetry", "run", "python", self.compiler_path, source_file, "-o", output_file], check=True)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as file:
            content = file.read()
            self.assertIn("result = (1 + 2)", content)

    def test_compiler_run_with_invalid_syntax_should_fail(self):
        source_file = os.path.join(self.input_directory, 'invalid_syntax.txt')
        output_file = os.path.join(self.output_directory, 'output_invalid_syntax.py')
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(["poetry", "run", "python", self.compiler_path, source_file, "-o", output_file], check=True)
