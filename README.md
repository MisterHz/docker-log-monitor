# Docker Log Monitor & Alert

> A plug-and-play observability stack for any application — logs, metrics, and email alerts in one `docker compose up`.

![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-v0.1%20happy%20path-blue)

---

## Status

🚧 In active development, built incrementally. **v0.1** ships the end-to-end log pipeline
(Loki + Promtail + Grafana + a demo app) on a single host. See the [Roadmap](#roadmap).

---

## What you get (v0.1)

- **Centralized logs** — every container's stdout/stderr collected automatically
- **Structured-log labels** — the demo app's JSON `level` (INFO/WARN/ERROR) becomes a Grafana label
- **Zero-touch Grafana** — Loki datasource auto-provisioned, env-driven URL
- **Demo app included** — a Flask service that emits realistic logs and simulates errors/latency

---

## Architecture

```
   ┌───────────┐   stdout/stderr   ┌────────────┐    push     ┌──────────┐
   │  demo-app │ ────────────────▶ │  Promtail  │ ──────────▶ │   Loki   │
   │  (Flask)  │   (Docker logs    │  (agent,   │   HTTP API  │  (logs)  │
   │   :8080   │    service disc.) │  docker_sd)│             │  :3100   │
   └───────────┘                   └────────────┘             └────┬─────┘
                                                                   │ query
                                                              ┌────┴─────┐
                                                              │ Grafana  │
                                                              │  :3000   │
                                                              └──────────┘
```

Promtail discovers containers via the Docker socket and ships their logs to Loki;
Grafana queries Loki through an auto-provisioned datasource.

---

## Quick Start

```bash
git clone https://github.com/MisterHz/docker-log-monitor.git
cd docker-log-monitor
docker compose up -d --build
```

Verify the pipeline:

```bash
# 1. Loki is ready
curl -s localhost:3100/ready          # -> ready

# 2. Generate some app traffic (INFO / WARN / ERROR)
curl -s localhost:8080/api/items      # 200 -> INFO
curl -s localhost:8080/api/items/9999 # 404 -> WARN
curl -s localhost:8080/api/error      # 500 -> ERROR

# 3. Open Grafana, then Explore -> Loki -> run:  {service="app"}
open http://localhost:3000             # login: admin / admin
```

Filter by level in Grafana, e.g. `{service="app", level="ERROR"}`.

### Endpoints

| Service  | URL                     | Notes                          |
|----------|-------------------------|--------------------------------|
| demo-app | http://localhost:8080   | `/api/items`, `/api/error`, `/api/slow`, `/api/random`, `/metrics` |
| Loki     | http://localhost:3100   | `/ready`, log query API        |
| Grafana  | http://localhost:3000   | login `admin` / `admin`        |

### Configuration

Overridable via environment (sane defaults built in):

| Variable                 | Default              | Purpose                          |
|--------------------------|----------------------|----------------------------------|
| `GRAFANA_ADMIN_USER`     | `admin`              | Grafana admin username           |
| `GRAFANA_ADMIN_PASSWORD` | `admin`              | Grafana admin password           |
| `LOKI_URL`               | `http://loki:3100`   | Loki URL the Grafana datasource points at (enables remote Loki later) |

---

## Plugging in your own app

Anything that logs to stdout is picked up automatically — no config needed.
To get a `level` label like the demo app, emit one JSON object per line:

```json
{"timestamp":"2026-06-03T11:17:47Z","level":"ERROR","service":"my-app","message":"boom"}
```

---

## Project layout

```
.
├── app/                    # demo Flask app — JSON logs + Prometheus /metrics
├── loki/                   # Loki single-binary config (filesystem storage)
├── promtail/               # Promtail config (Docker service discovery)
├── grafana/provisioning/   # auto-provisioned Loki datasource
├── docker-compose.yml
└── CHANGELOG.md
```

---

## Roadmap

- [x] **v0.1** — Happy path: Loki + Promtail + Grafana + demo app (1 compose, 1 host)
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

## License

[MIT](LICENSE) — use it, fork it, ship it.
