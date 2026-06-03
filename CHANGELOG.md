# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial project scaffolding (LICENSE, README skeleton, CHANGELOG, .gitignore)
- GitHub issue templates and PR template
- Loki single-binary service with filesystem storage (`docker-compose.yml`, `loki/loki-config.yml`)
- Promtail shipping Docker container stdout/stderr to Loki via Docker service discovery (`promtail/config.yml`)
- Grafana with auto-provisioned Loki datasource using an env-driven URL (`grafana/provisioning/`)
- Demo Python/Flask app emitting structured JSON logs (INFO/WARN/ERROR) with simulated error/slow/random endpoints (`app/`)
- README: Quick Start, architecture diagram, configuration, and project goals

---

<!--
Template for next release:

## [v0.X] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Removed
- ...
-->
