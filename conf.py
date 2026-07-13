"""Sphinx builder configuration file for dpic project."""

import os
import re
import requests

# --- Project Information ---
project = 'dpic'
copyright = '2004-2048, Dataist'
author = 'Hadi Mottale'

# --- Versioning Logic ---
# Dynamically reads the version from a local VERSION file.
current_dir = os.path.dirname(os.path.abspath(__file__))
version_file = os.path.join(current_dir, 'VERSION')

print(f"DEBUG: Looking for VERSION file at: {version_file}")

try:
    with open(version_file, 'r') as f:
        content = f.read().strip()
        # Extracts version if formatted as 'echo "x.x.x"'
        release = content.split('"')[1] if 'echo "' in content else content
except Exception as e:
    print(f"DEBUG: Error reading VERSION: {e}")
    release = '0.0.1'  # Fallback version

version = release
print(f"DEBUG: Version detected as: {release}")

# --- General Configuration ---
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
    '_build', 'Thumbs.db', '.DS_Store', 'README.md', '_source/download.tmpl.rst'
]

language = 'fa'
smartquotes = True

# --- HTML Theme & Interface ---
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
    'https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css'
]
html_js_files = [
    'https://code.jquery.com/jquery-3.6.0.min.js',
    'https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js',
    'js/datatable_init.js'
]
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.png'
html_search_language = 'fa'

html_theme_options = {
    'vcs_pageview_mode': 'edit',
    'logo_only': False,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
}

html_sidebars = {
    '**': ['searchbox.html', 'navigation.html', 'versions.html']
}

# --- Repository & Version Context ---
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

# --- Multi-Version Handling ---
smv_branch_whitelist = r'^(main|master|heuristic)$'
smv_tag_whitelist = r'^v\d+\.\d+(\.\d+)?$'
smv_released_pattern = r'^tags/.*$'
smv_remote_whitelist = None

# --- SEO & Sitemap ---
html_baseurl = 'https://dpic.dataist.ir/'
sitemap_url_scheme = "{link}"


# --- Automation: Checklist & Stats Engine ---

def download_checklist():
    """Fetches the latest remote checklist from GitHub.

    Downloads the checklist.rst file from the datapackverse repository
    and saves it to the local _templates/checklist directory for inclusion.
    """
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
    """Calculates statistics for the book and updates the download page.

    Iterates through the _source directory to count total words in RST/MD
    files and estimates the page count based on average word density.
    """
    total_words = 0
    source_dir = os.path.join(os.path.dirname(__file__), '_source')

    # Iterate through files to calculate word count
    if os.path.exists(source_dir):
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith(('.rst', '.md')) and file not in ['download.rst', 'download.tmpl.rst']:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = re.sub(r'.. \w+::.*', '', f.read())
                        content = re.sub(r':\w+:`.`', '', content)
                        total_words += len(re.findall(r'[\w\u200c]+', content))

    estimated_pages = max(1, round(total_words / 275))
    print(f"DEBUG: Words: {total_words}, Estimated Pages: {estimated_pages}")

    # Generate output file from template
    tmpl = os.path.join(source_dir, 'download.tmpl.rst')
    out = os.path.join(source_dir, 'download.rst')

    if os.path.exists(tmpl):
        with open(tmpl, 'r', encoding='utf-8') as f:
            data = f.read().replace('__TOTAL_WORDS_PLACEHOLDER__', f"{total_words:,}")
            data = data.replace('__ESTIMATED_PAGES_PLACEHOLDER__', str(estimated_pages))
        with open(out, 'w', encoding='utf-8') as f:
            f.write(data)

update_download_page_stats()

# --- LaTeX Configuration for Persian ---
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

# Global substitution for versioning in RST files
rst_prolog = f".. |version_number| replace:: {release}"
