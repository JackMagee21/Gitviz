import unittest
from utils.paths import figure_path

class FigurePathTests(unittest.TestCase):
    def test_relative_from_root(self):
        self.assertEqual(figure_path("", "src"), "src")

    def test_dotdot_moves_up(self):
        self.assertEqual(figure_path("src/utils", "../cmds"), "src/cmds")

    def test_absolute_ignores_current_path(self):
        self.assertEqual(figure_path("src", "/docs/"), "docs")

    def test_dot_stays_put(self):
        self.assertEqual(figure_path("src", "."), "src")

    def test_dotdot_cannot_go_above_root(self):
        self.assertEqual(figure_path("", ".."), "")

if __name__ == "__main__":
    unittest.main()
