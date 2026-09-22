from RepoData import set_repo
from cmds.cmd import cmd

import subprocess
import os


def clear_terminal():
    if os.name == "nt":  # Windows systems
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear")


clear_terminal()

current_repo = None

while True:
    repo_name = input("Enter repo author and name with a slash (/) in between "
                      "(e.g. name/repo_name), or press q to quit: ").strip()

    if repo_name.lower() == "q":
        break

    current_repo = set_repo(repo_name)
    if current_repo is None:
        print("Repo not found, please try again!")
    else:
        break

while current_repo is not None:
    user_input = input(current_repo.get_repo() + "> ").strip()
    parts = user_input.split(maxsplit=1)

    if not parts:          # empty input, ask again
        continue

    # Split the input into the command and any parameters
    command = parts[0].lower()
    parameters = parts[1] if len(parts) > 1 else ""

    if command == "q":
        break

    cmd(current_repo, command, parameters)