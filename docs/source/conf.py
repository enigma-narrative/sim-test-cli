import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = "mct"
copyright = "2026, Jeff Yurkiw"
author = "Jeff Yurkiw"

from mct import __version__ as release  # noqa: E402

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_static_path = ["_static"]
