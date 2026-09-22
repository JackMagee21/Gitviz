from cmds.help import help_cmd
from cmds.ls import cmd_ls
from cmds.info import cmd_info

def cmd(repo, command, parameters=""):
    if command == "help":
        print(help_cmd())
    elif command == "ls":
        print(cmd_ls(repo, parameters))
    elif command == "info":
        print(cmd_info(repo))
    else:
        print("Sorry, command not found")