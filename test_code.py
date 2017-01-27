#!/usr/bin/python3

import os
import shutil
import subprocess
from subprocess import PIPE
import pwd
import logging
from datetime import datetime
import sys
logging.basicConfig(level=logging.DEBUG)
import glob


# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('__main__')

def preexec_fn(username):
    uid = pwd.getpwnam(username).pw_uid
    os.setuid(uid)

def get_uid(username):
	username = pwd.getpwnam(username).pw_uid
	print('username: %s' % username)
	return username

def run_cmd(cmd, user='instructor'):
    """
    :param cmd: The command in the form of a list
    :param user: The name of the user who should run the process
    :return: The return code of the process
    """
    logger.debug('User %s about to run command %s' % (user, str(cmd)))
    p = subprocess.Popen(cmd, preexec_fn=preexec_fn(user),
                         stderr=PIPE, stdout=PIPE, )

    out, err = p.communicate()
    if out.decode('utf-8'):
        print(out.decode('utf-8'))
    if err:
        print(err.decode('utf-8'))

    return p.returncode

SUBMISSION_DIR = '/srv/nbgrader/exchange/data_science/inbound'
NBGRADER_DIR = '/home/huw/data_science'



def autograde_docker(username, assignment_name, instructor_id):
	# This function expects that there is a directory already in autograded/
	# If it doesn't exist, we should create it
	#TODO: Should probably have try/catch to remove it if we have a failed status code
	path = os.path.join(NBGRADER_DIR, 'autograded', username, assignment_name
	if not os.path.exists(path):
		os.makedirs(path)
	
    listy = [
        'docker', 'run', '-it', '--rm',
        '-v', '%s/submitted/%s:/home/instructor/user-submission/%s' 
        		% (NBGRADER_DIR, username, username),
        '-v', '%s/autograded/%s:/home/instructor/autograded-docker/%s' 
        		% (NBGRADER_DIR, username, username),
        '-v', '%s/gradebook.db:/home/instructor/gradebook.db' % NBGRADER_DIR,
        '-v', '%s/nbgrader_config.py:/home/instructor/nbgrader_config.py' % NBGRADER_DIR,
        '-v', '/home/instructor/students.csv:/home/instructor/students.csv',# % NBGRADER_DIR,
        'nbgrader-autograde-container',
        '/autograde', username, assignment_name, str(instructor_id)]
    run_cmd(listy, 'huw')


if __name__ == '__main__':
	autograde_docker('user-1', 'stats', get_uid('huw'))
