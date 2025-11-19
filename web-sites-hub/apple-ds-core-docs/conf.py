# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Data Structures Core'
copyright = '2025, Code Dojo'
author = 'Code Dojo'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'deploy', 'venv', 'README.md']

# The suffix of source filenames.
source_suffix = ['.rst', '.md']

# Myst parser configuration
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'dollarmath',
    'fieldlist',
    'html_admonition',
    'html_image',
    'replacements',
    'smartquotes',
    'strikethrough',
    'substitution',
    'tasklist',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 添加自定义 CSS
html_css_files = [
    'custom.css',
]

# 添加自定义 JavaScript
html_js_files = [
    'copy-code.js',
]

html_logo = None
# Favicon 将在下面配置（需要先导入 os）

# Theme options are theme-specific and customize the look and feel of a theme
html_theme_options = {
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Options for internationalization ----------------------------------------
language = 'en'
# locale_dirs = ['_locale/']
# gettext_compact = False

# -- Path setup --------------------------------------------------------------
import os
import sys
# 文件都在当前目录下，不需要添加上级目录路径

# -- Extension configuration -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Favicon 配置（需要放在这里，因为需要使用 os）---------------------------
if os.path.exists('_static/favicon.ico'):
    html_favicon = '_static/favicon.ico'
elif os.path.exists('_static/favicon.png'):
    html_favicon = '_static/favicon.png'
elif os.path.exists('_static/favicon.svg'):
    html_favicon = '_static/favicon.svg'
else:
    html_favicon = None

