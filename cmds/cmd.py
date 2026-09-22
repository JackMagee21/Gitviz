from cmds.help import help_cmd
from cmds.ls import cmd_ls

def cmd(repo, command, parameters=""):
    if command == "help":
        print(help_cmd())
    elif command == "ls":
        print(cmd_ls(repo, parameters))
    else:
        print("Sorry, command not found")