import subprocess
import os

def cmd_clear(parameters=""):
    if os.name == "nt": # For a windows system
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear")

