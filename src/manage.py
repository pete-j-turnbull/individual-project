import argparse
import runpy
import logging
import os
from importlib import import_module


parser = argparse.ArgumentParser()
parser.add_argument('prog')
parser.add_argument('--category', dest='category', default=None)
parser.add_argument('--settings', dest='settings', default=None)
parser.add_argument('--start_index', dest='start_item_index', default=0)

args = parser.parse_args()

os.environ['SETTINGS'] = args.settings
settings = import_module(os.environ['SETTINGS'])


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# create console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s: %(module)s:%(lineno)s %(funcName)s: %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# create error file handler and set level to error
handler = logging.FileHandler(os.path.join(settings.LOG_DIR, "error_%s%s.log" % (args.prog, args.category)), "a")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s: %(module)s:%(lineno)s %(funcName)s: %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# create debug file handler and set level to debug
handler = logging.FileHandler(os.path.join(settings.LOG_DIR, "debug_%s%s.log" % (args.prog, args.category)), "a")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s: %(module)s:%(lineno)s %(funcName)s: %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


#Run module with all settings stored as global
runpy.run_module(args.prog, init_globals={'CATEGORY': args.category, 'START_INDEX': args.start_item_index}, run_name=None, alter_sys=False)
