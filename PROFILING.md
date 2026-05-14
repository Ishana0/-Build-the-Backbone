# Baseline (before any fixes)

| Endpoint                | P50    | P95    | Error Rate |
|-------------------------|--------|--------|------------|
| GET /api/restaurants    | 75ms   | 140ms  | 0%         |
| GET /api/orders/history | 850ms  | 1450ms | 2%         |
| POST /api/orders        | 220ms  | 600ms  | 0%         |

---

# Findings

- `/api/orders/history` shows significantly higher latency than other endpoints.
- Multiple SQL queries indicate a likely N+1 query issue.
- Restaurant listing endpoint performs normally with low latency.
- Order history endpoint becomes the primary bottleneck under load.