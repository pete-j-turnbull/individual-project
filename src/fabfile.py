from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'pt1812'
env.hosts = ['shell1.doc.ic.ac.uk']

def run_worker():
    with cd('/homes/pt1812/Development/individual_project/src'):
    	run('../libs/fab -f fabfile_internal.py _run_worker')


