# 🚀 PostgreSQL Indexing Benchmark – Workflow Engine

## 📌 Objective

This project benchmarks the impact of indexing on a high-scale PostgreSQL database simulating a workflow automation system.

The goal is to demonstrate how proper indexing transforms query performance from seconds to milliseconds using realistic data and query patterns.

---

## 🗂️ Dataset Overview

Data was generated using generate_series to simulate a production-scale system.

### Table Sizes

| Table | Rows |
|------|------|
| regions | 20 |
| organizations | 500 |
| organization_units | 5,000 |
| users | 500,000 |
| teams | 25,000 |
| user_teams | 500,000 |
| roles | 2,500 |
| role_permissions | ~15,000 |
| user_roles | 500,000 |
| workflows | 200,000 |
| workflow_steps | 1,000,000 |
| workflow_regions | 200,000 |
| workflow_runs | 5,000,000 |
| workflow_logs | 15,000,000 |

---

## ⚙️ Benchmark Methodology

- Queries executed using EXPLAIN ANALYZE
- Same dataset used for before/after comparisons
- Focus on real-world query patterns
- Measured:
  - Execution time
  - Scan type
  - Rows processed

---

## 🧠 Indexing Strategy

Indexes were designed based on actual access patterns.

## Implemented Indexes

CREATE INDEX idx_org_units_org_region ON organization_units(org_id, region_id);

CREATE INDEX users_org_id_org_unit_id ON users(org_unit_id);

CREATE INDEX users_teams_team_id ON user_teams(team_id);

CREATE INDEX idx_workflows_org_unit_live ON workflows(org_unit_id, created_on DESC) WHERE is_deleted = false;

CREATE INDEX idx_workflows_org_live ON workflows(org_id, created_on DESC) WHERE is_deleted = false;

CREATE INDEX idx_workflow_region ON workflow_regions(region_id);

CREATE INDEX idx_workflow_runs_workflow ON workflow_runs(workflow_id, status, started_at DESC);

CREATE INDEX idx_workflow_log ON workflow_logs(workflow_run_id, execution_timestamp DESC);


---

## 📊 Performance Results

### Workflow Runs
Before: ~3107 ms → After: ~0.86 ms (~3500x faster)

### Workflow Logs
Before: ~2659 ms → After: ~0.10 ms (~24000x faster)

### Users
Before: ~326 ms → After: ~0.33 ms (~1000x faster)

### User Teams
Before: ~356 ms → After: ~0.17 ms (~2000x faster)

### Workflows
Before: ~165 ms → After: ~0.30 ms (~500x faster)

---

## 🔍 Key Observations

- Sequential scans are expensive on large datasets
- Composite indexes drastically improve performance
- Partial indexes reduce index size and improve speed
- Bitmap scans are efficient for medium result sets
- Small tables do not benefit from indexing
- UNIQUE and PRIMARY KEY automatically create indexes

---

## 📈 Conclusion

Indexing reduced query times from seconds to milliseconds, with improvements up to 24,000x.

---

## 🧩 Key Takeaways

- Index based on query patterns
- Use composite indexes for multi-column filters
- Use partial indexes for filtered datasets
- Validate with EXPLAIN ANALYZE
