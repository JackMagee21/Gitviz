import os
import sys

from colorama import Style

USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def color(text, fore):
    if not USE_COLOR:
        return text
    return f"{fore}{text}{Style.RESET_ALL}"