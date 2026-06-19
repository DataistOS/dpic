## DPIC (Dataist Professional Institute Certification)

This repository contains the source files and documentation for the **DPIC** book, built using Sphinx and localized for Persian (RTL).

---

### 🚀 Getting Started

#### Prerequisites
Make sure you have Python (>= 3.8) and Git installed on your system.

#### Installation
1. Clone the repository:

   ```bash
   git clone [https://github.com/DataistOS/dpic.git](https://github.com/DataistOS/dpic.git)
   cd dpic
   ```

2. Install dependencies (using the Iranian PyPI mirror to bypass restrictions):
   
   ```bash
   pip install sphinx myst-parser sphinx-rtd-theme sphinx-multiversion -i [https://mirror-pypi.runflare.com/simple](https://mirror-pypi.runflare.com/simple)
   ```

#### Build Commands

Depending on your needs, you can use one of the following commands to compile the documentation into HTML:

1. Draft Mode (Local Live Preview)

To compile your current untracked/local drafts without making a Git commit, use:
Bash

   ```bash
   sphinx-build -c . _source _build/html
   
   ```

Output location: _build/html/index.html

2. Multi-Version Mode (Production Build)
To build all Git branches and tags (e.g., main, master, heuristic) after committing your changes:
Bash

```bash
rm -rf _build/multiversion && sphinx-multiversion -c . _source _build/multiversion
   ```
Output location: _build/multiversion/

#
📂 Project Structure
```
Plaintext
├── _build/               # Compiled HTML outputs (Git ignored)
├── _source/              # Main book content (.rst files)
├── _static/              # Custom assets, CSS, and fonts
├── _templates/           # Sphinx HTML custom templates
├── conf.py               # Sphinx configuration file
└── README.md             # This documentation guide
```
#
✍️ Contribution Guide
- Create a new branch for your edits (e.g., git checkout -b feature/chapter-X).
- Write your content inside the _source/ directory using reStructuredText (RST).
- Keep Linux commands and syntax code blocks Left-to-Right (LTR).
- Verify the layout using the Draft Mode build command before sending a Merge Request.
