# ADR-001: Use Grafana Loki for logs, not the ELK/EFK stack

**Date:** 2026-06-03
**Status:** Accepted

## Context

The project needs centralized logging that a single developer can run on one host
today and grow into a multi-host, cloud-deployed setup later. The logging backend
sets the tone for resource footprint, operational burden, and how logs integrate
with the metrics/alerting added in later versions.

## Options Considered

1. **ELK / EFK** — Elasticsearch + Logstash (or Fluentd) + Kibana. Full-text
   indexing, very powerful search and analytics.
2. **Grafana Loki + Promtail + Grafana** — indexes only labels (not full log
   text); logs are stored as compressed chunks on the filesystem or object store.
3. **Hosted SaaS** — Datadog, CloudWatch Logs, etc. Minimal ops, usage-based cost.

## Decision

Use **Loki + Promtail + Grafana**.

## Why

- **Resource footprint.** Elasticsearch indexes every field and is JVM/heap-hungry;
  it is heavy for a single host. Loki indexes only labels, so it runs comfortably
  on a laptop and a small VM.
- **One pane of glass.** Metrics (Prometheus, added in v0.2) and logs share the
  same Grafana UI and a similar label model, instead of splitting across Kibana
  and a separate metrics tool.
- **Operational simplicity.** Single binary, filesystem storage to start, no
  cluster/shard/heap tuning to get a working pipeline.
- **Clean scale-out path.** The same Loki config swaps `filesystem` for S3/MinIO
  object storage later (v6.0) without changing the app or the agents.
- **Vendor neutrality.** Self-hosted and open source — no per-GB ingestion bill,
  which rules SaaS out for a portfolio/learning project.

## Trade-offs

- **Weaker full-text search.** Loki is built for label-scoped queries plus
  grep-style filtering, not the rich free-text search and aggregations Elasticsearch
  offers. Acceptable here: we query by service/level/time, not ad-hoc text mining.
- **Label cardinality discipline.** High-cardinality labels hurt Loki; dynamic
  values (request IDs, user IDs) must stay in the log line, not in labels.

## When to Reconsider

- Full-text search, log analytics, or complex aggregations become a core need.
- Non-Grafana consumers require an Elasticsearch-compatible API.
