# Baseline (before any fixes)

| Endpoint                | P50    | P95    | Error Rate |
|-------------------------|--------|--------|------------|
| GET /api/restaurants    | 75ms   | 140ms  | 0%         |
| GET /api/orders/history | 850ms  | 1450ms | 2%         |
| POST /api/orders        | 220ms  | 600ms  | 0%         |

---

# Query Count per Endpoint
 
| Endpoint                      | Query Count | Note                          |
|--------------------------------|-------------|-------------------------------|
| GET /api/restaurants          | 1           | Normal                        |
| GET /api/restaurants/:id/menu | 31          | ← N+1 query detected          |
| GET /api/orders/history       | 48          | ← Massive N+1 query detected  |

---

# EXPLAIN ANALYZE Results

### orders WHERE user_id = X

```sql
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 1
ORDER BY created_at DESC
LIMIT 20;
```

Seq Scan on orders
Rows Removed by Filter: 11800
Execution Time: 148ms

**Finding:** Sequential Scan on orders table  
**Rows scanned:** 12000  
**Execution time:** 148ms  
**Fix needed:** Missing index and N+1 query optimization

---

# Findings

- `/api/orders/history` showed significantly higher latency than other endpoints.
- Multiple SQL queries indicated severe N+1 query problems.
- Restaurant listing endpoint performed normally with low latency.
- Menu endpoint initially triggered repeated category queries.
- Order history endpoint became the primary bottleneck under load.