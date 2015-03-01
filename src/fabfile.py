from fabric.api import run, env, cd

#env.hosts += ['guest@146.169.47.6', 'guest@146.169.46.121', 'runuser@146.169.47.41']
env.gateway = 'shell1.doc.ic.ac.uk'
env.skip_bad_hosts = True
env.timeout=2


def run_worker():
	with cd('/homes/pt1812/Development/individual_project/src'):
		run("../libs/dtach -n `mktemp -u /tmp/dtach.XXXX` ../libs/celery worker -l info --concurrency=16")
