# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import re
from pathlib import Path
import os
import sys

sys.path.append(os.path.abspath('../..'))

init_path = Path(Path(__file__).parents[2], 'src', 'sciform', '__init__.py')
with open(init_path, 'r') as f:
    extracted_version = None
    for line in f.readlines():
        match = re.match(r'^__version__\s*=\s*(?P<version>("\d+\.\d+\.\d+"|\'\d+\.\d+\.\d+\')).*$', line)
        if match is not None:
            extracted_version = match.group('version')
            break
    if extracted_version is None:
        raise RuntimeError("Unable to find version string.")

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sciform'
copyright = '2023, Justin Gerber'
author = 'Justin Gerber'

version = extracted_version
release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo'
]

templates_path = ['_templates']
exclude_patterns = []

# autodoc_typehints = "description"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'navigation_depth': 4,
}
todo_include_todos = True

html_css_files = [
    'css/custom.css',
]