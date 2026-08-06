## [0.6.0] - 2026-08-06
### Added
- Add `rst_to_json.py` script in `_script/` to automate Docs-as-Code data extraction from `plan.rst` to JSON.
- Store generated `plan.json` under `_templates/docs_as_code/` directory.
### Changed
- Refactor business models and update `plan.rst` along with its dynamic JSON generation workflow.
- Update documentation for `dataflow` and `metasavalan` tools.
- Refresh ecosystem download guide and tools index (`download.rst` and `tools.rst`).
- Update `.gitignore` and `Makefile` configurations for build automation.
### Removed
- Remove legacy `plan.json` from the source business models directory.

## [v0.5.1] - 2026-07-30
### Changes & Improvements
- **Economy & Business Models (`plan.rst` & `plan.json`):**
  - Refined and structurally categorized role-based footnotes and citations across the revenue plan matrix.
  - Added structured business model definitions and configurations in the new `plan.json` file.
- **Documentation & Downloads (`download.rst`):**
  - Updated and optimized download guides and resource links.

## [0.5.0] - 2026-07-29
### Added
- Add documentation files for new tools:
  - `chatrang` (Interactive collaboration tool)
  - `clicord` (CLI coordination utility)
  - `daricaria` (Data management utility)
  - `dataistos` (Core DataistOS integration tool)
  - `gitchat` (Git-based communication utility)
  - `javidan` (Long-term data preservation tool)
  - `netarg` (Network argument analyzer)
  - `padra` (System management utility)
  - `peris` (Performance monitoring tool)
  - `persiatoon` (Animation and graphics utility)
  - `pirouz` (Victory and status tracker)
  - `surena` (Command-line automation utility)
  - `varg` (Validation and argument parser)
### Changed
- Update business models (`plan.rst`).
- Update existing tool documentation (`argenix`, `avand`, `bludreams`, `dataflow`, `datasync`, `dizhan`, `ganjor`, `github`, `haftkhan`, `hyperaryaland`, `idna`, `iranshahr`, `karnama`, `ketabek`, `neofetch`, `parsva`, `radin`, `rahnam`, `rastin`, `rayaname`, `rokhdad`, `rouz`, `vangah`, `vimist`).
- Update `download.rst` and `tools.rst` to integrate new ecosystem tools and configurations.
### Removed
- Remove deprecated map tool documentation (`rastin_map.rst`).

## [0.4.7] - 2026-07-21
### Added
- Add documentation files for new tools:
  - `argenix` (Smart pricing engine)
  - `avand` (Observability and system health tool)
  - `bludreams` (Sleep-focused tracker and community platform)
  - `dataflow` (GitHub Actions configurations for CI/CD)
  - `datasync` (Android data synchronization utility)
  - `github` (Configurations and templates)
  - `neofetch` (System information tool)
  - `parsva` (System backup and snapshot utility)
  - `rouz` (Calendar tool)
  - `vimist` (Vim/Neovim configuration)
### Changed
- Update `VERSION` to 0.4.7.
- Update `download.rst` and `tools.rst` to integrate new ecosystem tools and configurations.

## [0.4.6] - 2026-07-20
### Added
- **Documentation:** Added individual tool documentation pages for `dataiso`, `dizhan`, `haftkhan`, `hyperaryaland`, `iranshahr`, `karnama`, `ketabek`, `radin`, `rahnam`, `rastin`, `rastin_map`, `rayaname`, `rokhdad`, and `vangah`.
### Changed
- **Docs:** Updated `_source/tools.rst` and `_source/download.rst` to include and reference the newly added tools.
- **Version:** Bumped project version in `VERSION` to `0.4.6`.

## [0.4.4] - 2026-07-15
### Changed
- **Docs:** Updated `community.rst` to reflect the latest community engagement guidelines and structure.
- **Docs:** Refined `download.rst` to provide clearer access paths and resource links for the current distribution.
- **Maintenance:** General cleanup of information architecture in the community and download sections.
- 
## [0.4.3] - 2026-07-13
### Added
- Interactive sorting for ecosystem tool tables using DataTables.
- Custom initialization script (`_static/js/datatable_init.js`) for table UI cleanup.
### Changed
- Refined `conf.py` documentation and configuration to support dynamic table enhancements.
- Updated `VERSION` metadata.

## [0.4.0] - 2026-07-04
### Added / Updated
- **Version:** Bumped project version from `0.3.9` to `0.4.0`.
### Changes
- **Refactor:** Optimized core logic in `conf.py` and dynamic versioning system.
- **Documentation:** Corrected various typographical errors in `_source/tools.rst`.
- **General:** Improved stability and readability of documentation generation scripts.

## [0.3.9] - 2026-07-02
### Fixed
- Corrected `VERSION` file path resolution in `conf.py` to ensure accurate dynamic versioning.
- Fixed naming consistency by renaming `drsttrategies.rst` to `drstrategies.rst`.
### Changed
- Refactored `conf.py` to correctly locate the `VERSION` file within the local project root.
- Updated tool registry and project documentation.
### Added
- Initialized `CHANGELOG.md` to track project evolution.
