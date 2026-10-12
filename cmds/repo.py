def cmd_repo(repo, parameters=""):
    if parameters == "":
        print("Error: no repo name added, enter (for example) Author/Repo_name")
        return

    if not repo.switch_repo(parameters):
        print("Repo cannot be found")
