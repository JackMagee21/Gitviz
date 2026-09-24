import time

from github import Github, UnknownObjectException

git = Github()  # Limited to 60 requests per hour.

class RepoWrapper:
    def __init__(self, repo_name):
        self.repo = git.get_repo(repo_name)
        self.current_path = ""  # Start at the root of the repo.

    def get_repo(self):
        return self.repo.full_name

    def get_commits(self, count=10, path=""):
        # Returns the 10 most recent commits based on the path by default
        if path != "":
            all_commits = self.repo.get_commits(path=path)
        else:
            all_commits = self.repo.get_commits()

        return list(all_commits[:count])

    def get_stats_contributors(self, retries=5, delay=2):
        # GitHub computes contributor stats asynchronously. A None result means
        # "still generating" (HTTP 202) rather than "no contributors", so retry
        # a few times with a short pause before giving up.
        for attempt in range(retries):
            stats = self.repo.get_stats_contributors()
            if stats is not None:
                return stats
            time.sleep(delay)

        return None

    def switch_repo(self, repo):
        try:
            new_repo = git.get_repo(repo)
        except UnknownObjectException:
            return False

        self.repo = new_repo
        self.current_path = "" # Ensures that when a repo swaps it goes to the root of the new repo
        return True

    def get_file_content(self, file_path): 
        try:
            print(file_path)
            file_content = self.repo.get_contents(file_path)
            return file_content.decoded_content.decode("utf-8")
        except UnknownObjectException:
            return None

#returns an "empty none" object if the repo cannot be found 
def set_repo(repo_name):
    try:
        return RepoWrapper(repo_name)
    except UnknownObjectException:
        return None