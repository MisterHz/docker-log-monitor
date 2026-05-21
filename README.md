# Docker Log Monitor & Alert

> A plug-and-play observability stack for any application — logs, metrics, and email alerts in one `docker compose up`.

![License](https://img.shields.io/badge/license-MIT-green)

---

## Status

🚧 In active development. See [Roadmap](#roadmap) for current progress.

---

## Goals

- **Plug-and-play** — works with any app that writes log files or to stdout
- **Single-host first**, multi-host capable — start simple, scale when needed
- **Email alerts** — fire on application errors and resource exhaustion
- **Production-ready path** — TLS, secrets, scale-out documented at higher versions

---

## Roadmap

- [ ] **v0.1** — Happy path: Loki + Promtail + Grafana + demo app (1 compose, 1 host)
- [ ] **v0.2** — Metrics + email alerts (Prometheus + Node Exporter + Alertmanager)
- [ ] **v0.3** — Decoupled compose files (run subset of stack)
- [ ] **v1.0** — Multi-host topology (Promtail agent → remote Loki)
- [ ] **v1.1** — Developer experience (Makefile + setup wizard + doctor)
- [ ] **v2.0** — Cross-platform (macOS / Linux / Windows WSL2)
- [ ] **v3.0** — AWS EC2 deploy (manual)
- [ ] **v3.1** — GitHub Actions CI (config validation)
- [ ] **v3.2** — GitHub Actions CD (auto-deploy to EC2)
- [ ] **v4.0** — Non-Docker install option (bare-metal runbook)
- [ ] **v5.0** — Security hardening (TLS reverse proxy + secrets management)
- [ ] **v6.0** — Scale-out path (Loki + S3, OIDC deploy, k8s Helm chart)

---

## Quick Start

_Coming in v0.1._

---

## License

[MIT](LICENSE) — use it, fork it, ship it.
