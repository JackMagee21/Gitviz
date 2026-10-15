import os
os.environ["GITHUB_TOKEN"] = ""  # empty token: RepoData skips the real API call on import

import unittest
from unittest.mock import MagicMock, patch

import RepoData

def make_wrapper(**repo_attrs):
    # Builds a RepoWrapper around a fake PyGithub Repository, so no API calls are made.
    fake_repo = MagicMock(default_branch="main", **repo_attrs)
    with patch.object(RepoData, "git") as fake_git:
        fake_git.get_repo.return_value = fake_repo
        return RepoData.RepoWrapper("owner/name"), fake_repo

def make_entry(path):
    return MagicMock(path=path)

class GetCommitsTests(unittest.TestCase):
    def test_returns_10_commits_by_default(self):
        wrapper, _ = make_wrapper(get_commits=MagicMock(return_value=[MagicMock() for _ in range(25)]))
        self.assertEqual(len(wrapper.get_commits()), 10)

    def test_passes_path_through_to_github(self):
        wrapper, fake_repo = make_wrapper(get_commits=MagicMock(return_value=[]))
        wrapper.get_commits(path="src")
        fake_repo.get_commits.assert_called_once_with(path="src")

class GetFileContentTests(unittest.TestCase):
    def test_returns_decoded_text(self):
        item = MagicMock(size=5, decoded_content=b"hello")
        wrapper, _ = make_wrapper(get_contents=MagicMock(return_value=item))
        self.assertEqual(wrapper.get_file_content("a.txt"), ("hello", None))

    def test_directory_is_an_error(self):
        wrapper, _ = make_wrapper(get_contents=MagicMock(return_value=[MagicMock()]))
        content, error = wrapper.get_file_content("src")
        self.assertIsNone(content)
        self.assertEqual(error, "is a directory, not a file")

    def test_binary_file_is_an_error(self):
        item = MagicMock(size=2, decoded_content=b"\xff\xfe")
        wrapper, _ = make_wrapper(get_contents=MagicMock(return_value=item))
        content, error = wrapper.get_file_content("logo.png")
        self.assertIsNone(content)
        self.assertEqual(error, "binary file, not displayed")

    def test_too_large_file_is_an_error(self):
        item = MagicMock(size=RepoData.MAX_FILE_SIZE + 1)
        wrapper, _ = make_wrapper(get_contents=MagicMock(return_value=item))
        content, error = wrapper.get_file_content("big.log")
        self.assertIsNone(content)
        self.assertIn("too large", error)

class GetTreeTests(unittest.TestCase):
    def setUp(self):
        git_tree = MagicMock(raw_data={"truncated": False})
        git_tree.tree = [
            make_entry("src/a.py"),
            make_entry("src/b/c.py"),
            make_entry("srcfoo.txt"),  # must not match the "src" folder
            make_entry("README.md"),
        ]
        self.wrapper, self.fake_repo = make_wrapper(get_git_tree=MagicMock(return_value=git_tree))

    def test_whole_repo_when_no_path(self):
        entries, _, error = self.wrapper.get_tree()
        self.assertEqual(len(entries), 4)
        self.assertIsNone(error)

    def test_only_entries_under_path(self):
        entries, _, error = self.wrapper.get_tree("src")
        self.assertEqual([e.path for e in entries], ["src/a.py", "src/b/c.py"])
        self.assertIsNone(error)

    def test_missing_path_is_an_error(self):
        entries, _, error = self.wrapper.get_tree("docs")
        self.assertIsNone(entries)
        self.assertEqual(error, "no such file or directory")

if __name__ == "__main__":
    unittest.main()
