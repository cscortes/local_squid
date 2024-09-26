from io import StringIO
import unittest
import make as MK
import os 
import sys 
from unittest.mock import patch
from unittest.mock import mock_open, MagicMock


class TestParseMakefile(unittest.TestCase):
    def test_multiple_targets(self):
        """
        Test that multiple targets are parsed correctly.

        The expected result is a list of two target nodes, each containing the
        line number, target name, and commands associated with the target.
        """
        mkpath = os.path.join("OUTPUT",'test_multiple_targets.txt')
        expected_result = [
            MK.create_target_node(1, 'target1', [(2,'command1'), (3,'command2')]),
            MK.create_target_node(4, 'target2', [(5,'command3'), (6,'command4')])
        ]

        with open(mkpath, 'w') as f:
            f.write('target1:\n  command1\n  command2\ntarget2:\n  command3\n  command4')
        ans = MK.parse_makefile(mkpath)
        self.assertEqual(ans, expected_result)

    def test_single_target(self):
        """
        Test that a single target is parsed correctly.

        The expected result is a list with a single target node, containing the
        line number, target name, and commands associated with the target.
        """
        mkpath = os.path.join("OUTPUT",'test_single_targets.txt')
        expected_result = [
            MK.create_target_node(1, 'target1', [(2,'command1'), (3,'command2')])
        ]

        with open(mkpath, 'w') as f:
            f.write('target1:\n  command1\n  command2')
        ans = MK.parse_makefile(mkpath)
        self.assertEqual(ans, expected_result)

    def test_invalid_syntax(self):
        """
        Test that a Makefile with invalid syntax raises a ValueError.

        This test ensures that MK.parse_makefile() raises a ValueError when
        given a Makefile with invalid syntax. The expected result is a ValueError
        with a message indicating the invalid syntax.
        """
        mkpath = os.path.join("OUTPUT",'test_invalid_syntax.txt')
        with open(mkpath, 'w') as f:
            f.write(' invalid syntax ')

        with self.assertRaises(ValueError):
            ans = MK.parse_makefile(mkpath)        

#    @patch('builtins.open', side_effect=FileNotFoundError())
    def test_non_existent_makefile(self):
        """
        Test that a FileNotFoundError is raised when the Makefile does not exist.

        The expected result is a FileNotFoundError, indicating that the Makefile
        could not be found.
        """
        mkpath = os.path.join("OUTPUT",'non_existent_makefile.txt')
        with self.assertRaises(FileNotFoundError):
            MK.parse_makefile(mkpath)

class TestMakefile(unittest.TestCase):
    def test_list_targets(self):
        """
        Test that the --list command line parameter lists all targets in the Makefile.

        This test ensures that when the `--list` command line parameter is passed to the
        `make` command, it lists all targets in the Makefile. The expected result is a
        list of all targets in the Makefile.
        """
        with patch('builtins.open', mock_open(read_data='target1:\n  command1\n  command2\ntarget2:\n  command3\n  command4')):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                with self.assertRaises(SystemExit) as cm:
                    MK.main( 'make.py', ['--list'] )

        output = fake_stdout.getvalue().strip()
        self.assertEqual(output, 'Available targets:\n------------------\n\t- target1\n\t- target2')

    def test_non_existent_makefile(self):
        """ 
        Test that a FileNotFoundError is raised when the Makefile does not exist.

        The expected result is a FileNotFoundError, indicating that the Makefile
        could not be found.
        """
        with patch.object(MK, 'MAKEFILE_PATH', os.path.join("OUTPUT",'non_existent_makefile.txt')):
            with self.assertRaises(FileNotFoundError):
                MK.main( 'make.py', ['info'] )

    @patch('subprocess.run')
    def test_valid_target_name_on_command_line_found(self, mock_subprocess_run):
        """ 
        Test that a valid target name is found on the command line.
        """
        mock_subprocess_run.return_value.returncode = 0
        with patch('builtins.open', mock_open(read_data='target1:\n\n\n  command1')):
            with patch('sys.stdout', new=StringIO()) as fake_stdout:
                with self.assertRaises(SystemExit) as cm:
                    MK.main( 'make.py', ['target1'] )

        output = fake_stdout.getvalue().strip()
        self.assertEqual(output, "Executing commands for target 'target1'\nLine 1: # 4: command1")

class TestExecuteCommands(unittest.TestCase):
    @patch('subprocess.run')
    def test_execute_commands_success(self, mock_subprocess_run):
        """
        Test that execute_commands executes commands successfully.

        This test ensures that when the [execute_commands](cci:1://file:///c:/Users/MrLui/Code/local_squid/make.py:73:0-81:12) function is called with a
        list of commands, it executes each command and returns 0 if all commands are
        successful.
        """
        mock_subprocess_run.return_value.returncode = 0
        commands = [(10, 'command1',), (20, 'command2',)]
        result = MK.execute_commands('target', commands)
        self.assertEqual(result, 0)
        mock_subprocess_run.assert_called_with('command2', shell=True)

    @patch('subprocess.run')
    def test_execute_commands_failure(self, mock_subprocess_run):
        """
        Test that execute_commands returns 1 when a command fails.

        This test ensures that when the [execute_commands](cci:1://file:///c:/Users/MrLui/Code/local_squid/make.py:73:0-81:12) function is called with a
        list of commands, and one of the commands fails (i.e., returns a non-zero
        exit code), it returns 1.
        """
        mock_subprocess_run.return_value.returncode = 1
        commands = [(10, 'command1',), (20, 'command2',)]
        result = MK.execute_commands('target', commands)
        self.assertEqual(result, 1)
        mock_subprocess_run.assert_called_with('command1', shell=True)

    @patch('subprocess.run')
    def test_execute_commands_empty_commands(self, mock_subprocess_run):
        """
        Test that execute_commands returns 0 with empty commands.

        This test ensures that when the [execute_commands](cci:1://file:///c:/Users/MrLui/Code/local_squid/make.py:73:0-81:12) function is called with an
        empty list of commands, it returns 0.
        """
        commands = []
        result = MK.execute_commands('target', commands)
        self.assertEqual(result, 0)
        mock_subprocess_run.assert_not_called()


if __name__ == '__main__':
    unittest.main()