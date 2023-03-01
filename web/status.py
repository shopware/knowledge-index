import os

def get_status():
    status = {
        "status": "ok",
        "hash": None
    }

    commit_file = "commit.txt"
    if os.path.exists(commit_file):
        status["hash"] = open(commit_file, "rb").read()

    return status