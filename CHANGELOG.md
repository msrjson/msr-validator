<!-- version: 1.1.0 | build: 2026-09-20 | update: 2026-09-20 -->
# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning: [SemVer](https://semver.org/spec/v2.0.0.html). The version will be
declared in `pyproject.toml` with the first code; before `1.0.0` the API is
unstable and a MINOR release may break it.

## [Unreleased]

### Added

- Initial Python implementation: offline Draft 2020-12 validation against the
  schema generated from specification tag `v2.0.0`, with a SHA-256 pin and
  deterministic errors.

- The repository, with its role in the MSR JSON project, the one-way
  dependency direction and the rules its implementation must follow. No code
  and no release yet — see the README.
