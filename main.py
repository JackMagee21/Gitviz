from Repo import set_repo
from cmds.Commands import cmd

import subprocess
import os

found = False
user_input = ""

current_repo = None
repo_name = ""

def clear_terminal():
    if os.name == "nt": # Windows systems
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear')
    

clear_terminal()

while True:

    repo_name = input("Enter repo author and name with a slash (/) inbetween. (e.g name/repo_name), or press q to quit: ")
    current_repo = set_repo(repo_name)

    if repo_name.lower() == "q":
        break
    elif current_repo is None:
        print("Repo not found, please try again!")
    else:
        found = True
        break

while True: 
    if found == False: break

    user_input = input(current_repo.get_repo() + "> ")

    # quits the application
    if(user_input == "q"): break

    cmd(user_input)