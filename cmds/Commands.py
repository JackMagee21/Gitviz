from cmds.Help import help_cmd

def cmd(parameters):
    if(parameters == "help"):
        print(help_cmd())
    else:
        print("Sorry command not found")