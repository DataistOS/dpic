# Sphinx Builder Configuration File
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import requests

# -- Project Information -----------------------------------------------------
project = 'dpic'
copyright = ' 2004-2048, Dataist'
author = 'Hadi Mottale'
version = '0.0'
release = '0.3.8'

# -- General Configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx_design',
    'sphinx_sitemap',
    'sphinx_rtd_theme',
    'sphinx_copybutton',
    'sphinx_multiversion',
    'sphinx_last_updated_by_git',
]

sourcedir = '_source'
templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'README.md',
    '_source/download.tmpl.rst'  # Exclude the template file from direct rendering
]

language = 'fa'
smartquotes = True  # Automatically optimizes typography and double quotes

# -- HTML Output Options -----------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.png'
html_search_language = 'fa'

# -- Theme Options & Navigation ----------------------------------------------
html_theme_options = {
    'vcs_pageview_mode': 'edit',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
}

# -- Sidebar Templates Configuration -----------------------------------------
html_sidebars = {
    '**': [
        'searchbox.html',
        'navigation.html',
        'versions.html',  # Loads the custom multi-version switcher menu
    ]
}

# -- Git Integration & Flyout Menu Context -----------------------------------
html_context = {
    'display_github': True,
    'github_user': 'DataistOS',
    'github_repo': 'dpic',
    'github_version': 'main',
    'conf_py_path': '/',
    'github_host': 'github.com',
    'current_version': 'stable',
    'current_release': release,
    'versions': [('stable', '/'), ('latest', '/')],
    'downloads': [('HTML', '#'), ('EPUB', '#')],
}

# -- Sphinx Multiversion Configuration ----------------------------------------
smv_branch_whitelist = r'^(main|master|heuristic)$'
smv_tag_whitelist = r'^v\d+\.\d+(\.\d+)?$'
smv_released_pattern = r'^tags/.*$'
# Allow rebuilding from the local working directory without forcing remote checks
smv_remote_whitelist = None

# -- SEO Configuration (Sitemap) ---------------------------------------------
html_baseurl = 'https://dpic.dataist.ir/'
sitemap_url_scheme = "{link}"


# -- Dynamic Book Statistics and Checklist Generation ------------------------

# Fetches the latest checklist from the central repository and saves it to a template folder
def download_checklist():
    target_dir = os.path.join(os.path.dirname(__file__), '_templates', 'checklist')
    target_file = os.path.join(target_dir, 'checklist_remote.rst')
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    url = "https://raw.githubusercontent.com/DataistOS/datapackverse/heuristic/checklist.rst"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
    except Exception as e:
        print(f"Failed to fetch remote checklist: {e}")

download_checklist()

def update_download_page_stats():
    total_words = 0
    source_dir = os.path.join(os.path.dirname(__file__), '_source')

    # 1. Calculate total words from all source files
    if os.path.exists(source_dir):
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.rst') or file.endswith('.md'):
                    # Skip download files to avoid infinite loops or counting placeholders
                    if file in ['download.rst', 'download.tmpl.rst']:
                        continue

                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                        content = re.sub(r'.. \w+::.*', '', content)
                        content = re.sub(r':\w+:`.`', '', content)
                        words = re.findall(r'[\w\u200c]+', content)
                        total_words += len(words)

    estimated_pages = max(1, round(total_words / 275))

    print("=" * 50)
    print(f"DEBUG: TOTAL WORDS CALCULATED: {total_words}")
    print(f"DEBUG: ESTIMATED PAGES CALCULATED: {estimated_pages}")
    print("=" * 50)

    # 2. Read from Template and write freshly to download.rst
    template_path = os.path.join(source_dir, 'download.tmpl.rst')
    download_file_path = os.path.join(source_dir, 'download.rst')

    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # Replace placeholders dynamically
        rendered_content = template_content.replace('__TOTAL_WORDS_PLACEHOLDER__',
                                                    f"{total_words:,}")
        rendered_content = rendered_content.replace('__ESTIMATED_PAGES_PLACEHOLDER__',
                                                    str(estimated_pages))

        with open(download_file_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)


# Run the stats engine on build
update_download_page_stats()

# -- LaTeX Options for Persian Language Support ------------------------------
latex_engine = 'xelatex'
latex_elements = {
    'fontpkg': '',
    'fontenc': '',
    'geometry': r'\geometry{a4paper,margin=2.5cm}',
    'preamble': r'''
        \usepackage{geometry}
        \usepackage{fontspec}
        \usepackage{bidi}
        \setmainfont{FreeSans}
    ''',
}

# Global substitution for the current release version
rst_prolog = f"""
.. |version_number| replace:: {release}
"""
