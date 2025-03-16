# Changelog

## [0.2.13] - 2024-03-24

### Fixed
- Fixed ModuleNotFoundError for _models package by updating setuptools configuration to automatically discover all packages

## [0.2.12] - 2024-03-24

### Added
- Added structured Idiom model with etymology, senses, and examples
    - Added Sense model for representing idiom definitions and usage examples
    - Added source URL tracking for each idiom
- Added new dev dependencies: pydantic, pyyaml, openai, pandas, python-dotenv, requests

### Changed
- Reorganized scripts directory structure (moved readme scripts to dedicated folder)
- Migrated idiom storage to YAML format with full linguistic information
