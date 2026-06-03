import json
import os
import random
import time
import uuid
import logging
from datetime import datetime, timezone

from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

SERVICE_NAME = os.getenv("SERVICE_NAME", "demo-app")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)


def json_log(level: str, message: str, request_id: str = "-", duration_ms: float = 0, **extra):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level.upper(),
        "service": SERVICE_NAME,
        "request_id": request_id,
        "message": message,
        "duration_ms": round(duration_ms, 2),
    }
    entry.update(extra)
    print(json.dumps(entry), flush=True)


@app.before_request
def start_timer():
    request.start_time = time.time()
    request.request_id = str(uuid.uuid4())


@app.after_request
def log_and_record(response):
    duration_ms = (time.time() - request.start_time) * 1000
    endpoint = request.url_rule.rule if request.url_rule else request.path

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status_code=str(response.status_code),
    ).inc()
    REQUEST_DURATION.labels(method=request.method, endpoint=endpoint).observe(duration_ms / 1000)

    level = "ERROR" if response.status_code >= 500 else "WARN" if response.status_code >= 400 else "INFO"
    json_log(
        level=level,
        message=f"{request.method} {endpoint} → {response.status_code}",
        request_id=request.request_id,
        duration_ms=duration_ms,
        http_method=request.method,
        http_path=endpoint,
        http_status=response.status_code,
    )
    return response


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME})


@app.route("/api/items")
def list_items():
    items = [{"id": i, "name": f"Item {i}", "price": round(random.uniform(1, 100), 2)} for i in range(1, 11)]
    return jsonify({"items": items, "total": len(items)})


@app.route("/api/items/<int:item_id>")
def get_item(item_id):
    if item_id < 1 or item_id > 100:
        return jsonify({"error": "Item not found", "item_id": item_id}), 404
    return jsonify({"id": item_id, "name": f"Item {item_id}", "price": round(random.uniform(1, 100), 2)})


@app.route("/api/slow")
def slow_endpoint():
    delay = random.uniform(0.5, 3.0)
    time.sleep(delay)
    return jsonify({"message": "Slow response", "delay_ms": round(delay * 1000, 2)})


@app.route("/api/error")
def error_endpoint():
    json_log("ERROR", "Simulated internal error", request_id=request.request_id)
    return jsonify({"error": "Internal server error", "code": "ERR_SIMULATED"}), 500


@app.route("/api/random")
def random_endpoint():
    r = random.random()
    if r < 0.1:
        return jsonify({"error": "Random failure"}), 500
    if r < 0.25:
        time.sleep(random.uniform(1.0, 2.5))
    return jsonify({"value": random.randint(1, 1000), "at": datetime.now(timezone.utc).isoformat()})


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    json_log("INFO", "Starting demo-app", port=8080)
    app.run(host="0.0.0.0", port=8080, debug=False)
