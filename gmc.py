#!/usr/bin/env python

import argparse
import os
import subprocess

# settings
CMD_FILETYPES           = { 'main.py': 'python', 'main.sh': 'sh', 'main': 'sh' }
SEARCH_DIRS             = ['/Users/gmcclure/bin/gmc_src']

# messages
CMD_NOT_FOUND_MSG       = 'Command not found in following directories:'
CMD_NOT_FOUND_LIST_TMPL = ' -> {}'
ERR_CODE_TMPL           = 'Error code {} -> {}'
NO_CMD_MSG              = 'No command given.\n'
SEARCH_DIR_FALSE_TMPL   = 'Search directory "{}" does not exist.'

parser = argparse.ArgumentParser(description='Namespace custom scripts.')
parser.add_argument('command', metavar='cmd', type=str, nargs='*', 
        help='name of an executable script stored in a preset directory')

args = parser.parse_args()

def exec_cmd(cmd_list):
    cmd_found = False
    cmd_path  = ''
    cmd_file  = ''
    ret       = 1

    for c_dir in SEARCH_DIRS:
        if not os.path.exists(c_dir):
            print SEARCH_DIR_FALSE_TMPL.format(c_dir)
            continue

        for cmd in CMD_FILETYPES.keys():
            if os.path.exists(os.path.join(c_dir, cmd_list[0], cmd)):
                cmd_found = True
                cmd_file  = cmd
                cmd_path  = os.path.join(c_dir, cmd_list[0], cmd)
                break

    if not cmd_found:
        print CMD_NOT_FOUND_MSG
        for c_dir in SEARCH_DIRS:
            print CMD_NOT_FOUND_LIST_TMPL.format(c_dir)
    else:
        command = ' '.join([CMD_FILETYPES[cmd_file]] + [cmd_path] + cmd_list[1:])
        try:
            ret = subprocess.check_call(command, shell=True)
        except OSError as err:
            print command
            print ERR_CODE_TMPL.format(err.errno, err.strerror)

    return ret

if (len(args.command) == 0):
    print NO_CMD_MSG
    parser.print_help()
else:
    exec_cmd(args.command)
