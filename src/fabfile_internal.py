from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['pixel01, edge12']

def _run_worker():
    with cd('/homes/pt1812/Development/individual_project/src'):
    	run('nohup ../libs/celery worker -l info --concurrency=8 &')

