#!/usr/bin/python

import glob
import json
import os
import pwd
import shutil
import socket
import subprocess



def run_tests(module, result):
    install_testing_dependencies(module)

    local_client_git_dir = os.path.expanduser('~/jargon')
    git_clone(module, local_client_git_dir)

    module.run_command('python-coverage run irods/test/runner.py', cwd=local_client_git_dir, check_rc=True)
    module.run_command('python-coverage report', cwd=local_client_git_dir, check_rc=True)
    module.run_command('python-coverage xml', cwd=local_client_git_dir, check_rc=True)

    gather_xml_reports(module, local_client_git_dir)

def install_testing_dependencies(module):
    module.run_command('sudo apt-get update', check_rc=True)
    packages = ['git', 'python-prettytable', 'python-coverage']
    install_command = ['sudo', 'apt-get', 'install', '-y'] + packages
    module.run_command(install_command, check_rc=True)

def git_clone(module, local_dir, commit=None):
    module.run_command('git clone --recursive {0} {1}'.format(module.params['python_client_git_repository'], local_dir), check_rc=True)
    module.run_command('git checkout {0}'.format(module.params['python_client_git_commitish']), cwd=local_dir, check_rc=True)

def gather_xml_reports(module, local_client_git_dir):
    shutil.copy(os.path.join(local_client_git_dir, 'coverage.xml'), module.params['output_directory'])

def main():
    module = AnsibleModule(
        argument_spec = dict(
            output_directory=dict(type='str', required=True),
            python_client_git_repository=dict(type='str', required=True),
            python_client_git_commitish=dict(type='str', required=True),
        ),
        supports_check_mode=False,
    )

    result = {}
    run_tests(module, result)

    result['changed'] = True
    result['complex_args'] = module.params

    module.exit_json(**result)


from ansible.module_utils.basic import *
main()
