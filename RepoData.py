from github import Github, UnknownObjectException

git = Github()  # Limited to 60 requests per hour.

class RepoWrapper:
    def __init__(self, repo_name):
        self.repo = git.get_repo(repo_name)
        self.current_path = ""  # Start at the root of the repo.

    def get_repo(self):
        return self.repo.full_name

#returns an "empty none" object if the repo cannot be found 
def set_repo(repo_name):
    try:
        return RepoWrapper(repo_name)
    except UnknownObjectException:
        return None