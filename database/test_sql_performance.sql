-- =========================================================
-- ANALYZE
-- =========================================================

VACUUM ANALYZE;

-- =========================================================
-- BENCHMARK BEFORE EXTRA INDEXES
-- =========================================================

-- Indexing not needed for regions, as sql will mostly prefer full table scan, as the table is small

EXPLAIN ANALYZE
SELECT * 
FROM regions;

-- =========================================================

-- Indexing not needed as unique constraint name already creates an index 

EXPLAIN ANALYZE
SELECT * 
FROM organizations
WHERE name = 'Organization 30';


EXPLAIN ANALYZE
SELECT * 
FROM organization_units
WHERE org_id = '32';


EXPLAIN ANALYZE
SELECT * 
FROM organization_units
WHERE org_id = '29'
AND region_id = '9';


-- =========================================================

-- Users

EXPLAIN ANALYZE
SELECT *
FROM users
WHERE email = 'user134280@mail.com'


EXPLAIN ANALYZE
SELECT *
FROM users;

EXPLAIN ANALYZE
SELECT *
FROM users
WHERE org_id = '47'
AND org_unit_id = '4287';

-- =========================================================

-- User teams

EXPLAIN ANALYZE
SELECT * FROM user_teams
WHERE team_id = '12';

-- =========================================================

-- Workflows

EXPLAIN ANALYZE
SELECT * FROM workflows
WHERE org_id = '22'
AND is_active = true
ORDER BY created_on DESC;

EXPLAIN ANALYZE
SELECT * FROM workflows
WHERE org_unit_id = '5'
AND is_active = true
ORDER BY created_on DESC;

EXPLAIN ANALYZE
SELECT * FROM workflows
WHERE id = '21';

EXPLAIN ANALYZE
SELECT * FROM workflow_steps
WHERE workflow_id = '31'

CREATE INDEX idx_workflow_region
ON workflow_regions(region_id);

EXPLAIN ANALYZE
SELECT * FROM workflow_regions
WHERE region_id = '32'

-- =========================================================


CREATE INDEX idx_workflow_runs_workflow
ON workflow_runs(workflow_id, status, started_at DESC);


EXPLAIN ANALYZE
SELECT *
FROM workflow_runs
WHERE workflow_id = 1500;

EXPLAIN ANALYZE
SELECT *
FROM workflow_runs
WHERE workflow_id = 1500 
AND status='failed'
ORDER BY started_at DESC
LIMIT 100;



-- =========================================================


CREATE INDEX idx_workflow_log
ON workflow_lo(workflow_run_id, execution_timestamp DESC);


EXPLAIN ANALYZE
SELECT *
FROM workflow_logs
WHERE workflow_run_id = 298884
ORDER BY execution_timestamp DESC;

VACUUM ANALYZE;

