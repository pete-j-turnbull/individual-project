from fabric.api import run, env, cd

env.user = 'pt1812'
env.hosts = ['shell1.doc.ic.ac.uk']

def run_worker():
    with cd('/homes/pt1812/Development/individual_project/src'):
    	run('../libs/fab -f fabfile_internal.py run_worker')


