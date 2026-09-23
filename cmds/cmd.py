from cmds.help import help_cmd
from cmds.ls import cmd_ls
from cmds.info import cmd_info
from cmds.cd import cmd_cd
from cmds.logs import cmd_log
from cmds.repo import cmd_repo

def cmd(repo, command, parameters=""):
    if command == "help":
        print(help_cmd())
    elif command == "ls":
        print(cmd_ls(repo, parameters))
    elif command == "info":
        print(cmd_info(repo))
    elif command == "cd":
        cmd_cd(repo, parameters)
    elif command == "log":
        cmd_log(repo, parameters)
    elif command == "repo":
        cmd_repo(repo, parameters)
    else:
        print("Sorry, command not found")