import subprocess
import re
import sys
from typing import List, Dict

MAKEFILE_PATH = 'Makefile'
TARGET_PAT = r'^[a-zA-Z0-9_]+:'

# function to create a dictionary from line, line number, and target
def create_target_node(line_number, target, commands=[]):
    """
    Creates a target node, which is a dictionary containing target information.

    Parameters:
        target (str): the target name
        line_number (int): the line number in the Makefile
        commands (list): a list of (line_number, command as string) tuples

    Returns:
        dict: a target node dictionary
    """
    return {
        'target': target,
        'line_number': line_number,
        'commands': commands	
    }

def parse_makefile(mkpath: str) -> List[Dict]:
    """
    Parse Makefile into a list of target nodes.

    Parameters:
        mkpath (str): path to Makefile

    Returns:
        List[Dict]: a list of target nodes

    The target node is a dictionary containing target information.
    The target node dictionary contains the following keys:
        - target (str): the target name as a string
        - line_number (int): the line number in the Makefile
        - commands (List[str]): a list of strings representing commands associated with the target
    """
    target: str = None
    target_linenum: int = 0
    commands: List[str] = []
    target_nodes: List[Dict] = []

    with open(mkpath, 'r') as makefile:
        text = makefile.read()

    for line_number, line in enumerate(text.splitlines(),1):
        line = line.strip()

        if re.match(TARGET_PAT, line): # Found a Target
            if target is not None:
                target_nodes.append(create_target_node(target_linenum, target, commands))
            target = line[:-1]
            commands = []
            target_linenum = line_number
        else:                           # Found a Command
            if (not line) or (line.startswith('#')):
                continue
            commands.append((line_number, line))
            
    # Add the last target's commands to the list
    if target is not None:
        target_nodes.append(create_target_node(target_linenum, target, commands))
    elif  commands != []:
        raise ValueError('Invalid syntax in Makefile')
    
    return target_nodes

def execute_commands(target, commands):
    """Executes the given commands and returns the exit code."""
    print(f"Executing commands for target '{target}'")
    for idx, (line_num, command) in enumerate(commands, 1):
        print(f"Line {idx}: # {line_num}: {command}")
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print(f"Command failed with exit code {result.returncode}")
            return result.returncode
    return 0

def main(prog, args):

    if len(args) < 1:
        print(f"Usage: python {prog} <target>")
        sys.exit(1)

    target = args[0]
    targets = parse_makefile(MAKEFILE_PATH)
    
    if len(args) == 1 and args[0] == '--list':
        print("Available targets:")
        print("------------------")
        for target in targets:
            print(f"\t- {target['target']}")
        sys.exit(0)


    # search for target in targets
    for t in targets:
        if t['target'] == target:
            found_target = t
            break   
    else:
        raise ValueError(f"Target '{target}' not found in Makefile")


    exit_code = execute_commands(target, found_target['commands'])
    sys.exit(exit_code)

if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
