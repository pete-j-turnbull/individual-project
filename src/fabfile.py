from fabric.api import run, env, cd

env.user = 'pt1812'
env.hosts = ['pixel01.doc.ic.ac.uk']
env.gateway = 'shell1.doc.ic.ac.uk'

def run_worker():
    with cd('/homes/pt1812/Development/individual_project/src'):
    	run('nohup ../libs/celery worker -l info --concurrency=16 &')

