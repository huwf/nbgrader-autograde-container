#!/usr/bin/python3

import os
import shutil
import subprocess
from subprocess import PIPE
import pwd
import logging
from datetime import datetime
import sys
import glob

SUBMISSION_DIR = '/srv/nbgrader/exchange/data_science/inbound'
NBGRADER_DIR = '/home/instructor/data_science'
ASSIGNMENT = sys.argv[1]
print('ASSIGNMENT: ', ASSIGNMENT)

import os
os.chdir(os.path.join('/home', 'instructor', 'data_science'))



logging.basicConfig(level=logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('__main__')

def preexec_fn(username):
    uid = pwd.getpwnam(username).pw_uid
    os.setuid(uid)


def get_uid(username):
    username = pwd.getpwnam(username).pw_uid
    logger.debug('username: %s' % username)
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


from nbgrader.apps import *
from six import StringIO


def collect(assignment_name, exchange='/srv/nbgrader/exchange'):
    app = CollectApp.instance()
    log_buff = StringIO()
    app.init_logging(logging.StreamHandler, [log_buff], color=False, subapps=True)
    app.course_id = 'data_science'
    app.initialize(['%s' % assignment_name, '--TransferApp.exchange_directory=%s' % exchange, '--update', '--debug'])
    app.start()
    out = log_buff.getvalue()
    log_buff.close()
    src_records = app.src_records
    app = None

    return src_records

def autograde_docker(username, assignment_name, instructor_id):
    # This function expects that there is a directory already in autograded/
    # If it doesn't exist, we should create it
    #TODO: Should probably have try/catch to remove it if we have a failed status code
    path = os.path.join(NBGRADER_DIR, 'autograded', username, assignment_name)
    if not os.path.exists(path):
        os.makedirs(path)

    listy = [
    'docker', 'run', '-it', '--rm',
    '--net=jupyterhub',
    '-v', '%s/submitted/%s:/home/instructor/user-submission/%s'
        % (NBGRADER_DIR, username, username),
    '-v', '%s/autograded/%s:/home/instructor/autograded-docker/%s'
        % (NBGRADER_DIR, username, username),
    '-v', '/srv/nbgrader/exchange:/srv/nbgrader/exchange',
    # '-v', '%s/gradebook.db:/home/instructor/gradebook.db' % NBGRADER_DIR,
    '-v', '%s/nbgrader_config.py:/home/instructor/nbgrader_config.py' % NBGRADER_DIR,
    '-v', '/home/huw/docker/nbgrader-autograde-container/data_science:/home/instructor/data_science',# % NBGRADER_DIR,
    '-e', 'GRADEBOOK_DB=postgresql+psycopg2://nbgraderuser:U7092SKDDFvp@postgres_container:5432/gradebook',
    'huwf/nbgrader-autograde-container',
    #'bash'
    '/autograde', username, assignment_name, str(instructor_id)]
    run_cmd(listy, 'root')


if __name__ == '__main__':
    if not os.path.exists('%s/backup' % NBGRADER_DIR):
        os.makedirs('%s/backup' % NBGRADER_DIR)
#    for assignment in os.listdir('/srv/nbgrader/exchange/data_science/outbound'):
#        logger.info('Collecting assignments for %s' % assignment)
    for src in collect(ASSIGNMENT):
        print('src', src)
        autograde_docker(src['username'], ASSIGNMENT, get_uid('instructor'))
        print('src', src['filename'])
        shutil.move('%s/%s' % (SUBMISSION_DIR, src['filename']), '%s/backup' % NBGRADER_DIR)
        


