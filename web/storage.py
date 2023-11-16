import subprocess
from .config import data_dir, cache_dir, db_dir
from glob import glob

def get_storage_info():
    # add default dirs
    dirs = [
        data_dir(None),
        cache_dir(),
        db_dir(None)
    ]

    # discover extra dirs
    for dir in glob("/data/*/", recursive = False):
        dirs.append(dir.rstrip("/"))

    # get dir sizes
    result = {}
    for dir in dirs:
        result[dir] = subprocess.check_output(['du', '-sh', dir]).split()[0].decode('utf-8')

    return result