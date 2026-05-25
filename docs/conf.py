import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'PyDREAM'
copyright = '2016-2024, Erin Shockley, Benjamin Zoller, et al.'
author = 'Erin Shockley, Benjamin Zoller, et al.'
version = '2.0'
release = '2.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '*/tests/*', '*/examples/*']

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
master_doc = 'index'

html_theme = 'furo'
html_static_path = ['_static']

# Napoleon settings for parsing NumPy-style docstrings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
