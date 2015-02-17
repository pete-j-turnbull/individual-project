sys.path.append('../libs/fabric')
from api import run, env, cd

env.hosts = ['pixel01']

def run_worker():
    with cd('/homes/pt1812/Development/individual_project/src'):
    	run('nohup ../libs/celery worker -l info --concurrency=16 &')

