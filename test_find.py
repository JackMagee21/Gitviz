import unittest
from types import SimpleNamespace

from cmds.find import cmd_find


class FakeRepo:
    # Stands in for RepoWrapper so the tests never hit the API
    def __init__(self, paths, current_path=""):
        self.current_path = current_path
        self.entries = [SimpleNamespace(path=x.rstrip("/"), type="tree" if x.endswith("/") else "blob")
                        for x in paths]

    def get_tree(self, path=""):
        # Same filtering as RepoWrapper.get_tree
        matches = [e for e in self.entries
                   if not path or e.path == path or e.path.startswith(path + "/")]
        return matches, False, None


PATHS = ["src/", "src/utils/", "src/utils/paths.py", "src/cmds/", "src/cmds/find.py", "README.md"]


class FindTests(unittest.TestCase):
    def test_plain_word_matches_anywhere_in_name(self):
        result = cmd_find(FakeRepo(PATHS), "paths")
        self.assertEqual(result, "/src/utils/paths.py")

    def test_wildcard_matches_extension(self):
        result = cmd_find(FakeRepo(PATHS), "*.py")
        self.assertEqual(result, "/src/cmds/find.py\n/src/utils/paths.py")

    def test_match_is_case_insensitive(self):
        result = cmd_find(FakeRepo(PATHS), "readme")
        self.assertEqual(result, "/README.md")

    def test_slash_pattern_matches_path_relative_to_here(self):
        result = cmd_find(FakeRepo(PATHS, current_path="src"), "utils/*")
        self.assertEqual(result, "/src/utils/paths.py")

    def test_searches_from_current_directory_only(self):
        result = cmd_find(FakeRepo(PATHS, current_path="src/cmds"), "*")
        self.assertEqual(result, "/src/cmds/find.py")

    def test_no_match_says_so(self):
        self.assertEqual(cmd_find(FakeRepo(PATHS), "nope"), "find: no matches for 'nope'")

    def test_empty_pattern_shows_usage(self):
        self.assertTrue(cmd_find(FakeRepo(PATHS), "").startswith("find: give a name"))


if __name__ == "__main__":
    unittest.main()
