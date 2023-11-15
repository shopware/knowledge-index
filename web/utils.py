import os

def safe_dir(root: str, dir: str):
    fullpath = os.path.normpath(os.path.join(root, dir))

    if not fullpath.startswith(root):
        raise Exception("Incorrect path")
    
    return fullpath

def safe_dir_append(root: str, dir: str):
    fullpath = os.path.normpath(root + dir)

    if not fullpath.startswith(root):
        raise Exception("Incorrect path")
    
    return fullpath