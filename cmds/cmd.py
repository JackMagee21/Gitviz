from cmds.help import help_cmd
from cmds.ls import cmd_ls
from cmds.info import cmd_info
from cmds.cd import cmd_cd

def cmd(repo, command, parameters=""):
    if command == "help":
        print(help_cmd())
    elif command == "ls":
        print(cmd_ls(repo, parameters))
    elif command == "info":
        print(cmd_info(repo))
    elif command == "cd":
        cmd_cd(repo, parameters)
    else:
        print("Sorry, command not found")