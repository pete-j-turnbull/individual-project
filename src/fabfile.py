from fabric.api import run, env, cd

env.hosts = ['pt1812@edge01.doc.ic.ac.uk','pt1812@edge02.doc.ic.ac.uk','pt1812@edge03.doc.ic.ac.uk','pt1812@edge04.doc.ic.ac.uk','pt1812@edge21.doc.ic.ac.uk',
				'pt1812@edge06.doc.ic.ac.uk','pt1812@edge07.doc.ic.ac.uk','pt1812@edge08.doc.ic.ac.uk','pt1812@edge09.doc.ic.ac.uk','pt1812@edge10.doc.ic.ac.uk',
				'pt1812@edge11.doc.ic.ac.uk','pt1812@edge12.doc.ic.ac.uk','pt1812@edge13.doc.ic.ac.uk','pt1812@edge14.doc.ic.ac.uk','pt1812@edge15.doc.ic.ac.uk',
				'pt1812@edge16.doc.ic.ac.uk','pt1812@edge17.doc.ic.ac.uk','pt1812@edge18.doc.ic.ac.uk','pt1812@edge19.doc.ic.ac.uk','pt1812@edge20.doc.ic.ac.uk']
#env.hosts += ['guest@146.169.47.6', 'guest@146.169.46.121', 'runuser@146.169.47.41']
env.gateway = 'shell1.doc.ic.ac.uk'
env.skip_bad_hosts = True
env.timeout=2


def run_worker():
    with cd('/homes/pt1812/Development/individual_project/src'):
    	run("../libs/dtach -n `mktemp -u /tmp/dtach.XXXX` ../libs/celery worker -l info --concurrency=16")
