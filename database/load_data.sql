-- =========================================================
-- WORKFLOW_ENGINE HIGH-SCALE TEST DATA LOADER (UPDATED DDL)
-- Respects UNIQUE / FK constraints
-- Optimized for benchmarking indexes & query performance
-- =========================================================

\c workflow_engine;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

SET maintenance_work_mem = '1GB';
SET work_mem = '256MB';
SET synchronous_commit = off;
SET temp_buffers = '256MB';

-- =========================================================
-- OPTIONAL CLEAN LOAD
-- =========================================================

TRUNCATE TABLE workflow_logs RESTART IDENTITY CASCADE;
TRUNCATE TABLE workflow_runs RESTART IDENTITY CASCADE;
TRUNCATE TABLE workflow_regions RESTART IDENTITY CASCADE;
TRUNCATE TABLE workflow_steps RESTART IDENTITY CASCADE;
TRUNCATE TABLE workflows RESTART IDENTITY CASCADE;
TRUNCATE TABLE user_roles RESTART IDENTITY CASCADE;
TRUNCATE TABLE role_permissions RESTART IDENTITY CASCADE;
TRUNCATE TABLE permissions RESTART IDENTITY CASCADE;
TRUNCATE TABLE roles RESTART IDENTITY CASCADE;
TRUNCATE TABLE user_teams RESTART IDENTITY CASCADE;
TRUNCATE TABLE teams RESTART IDENTITY CASCADE;
TRUNCATE TABLE users RESTART IDENTITY CASCADE;
TRUNCATE TABLE organization_units RESTART IDENTITY CASCADE;
TRUNCATE TABLE organizations RESTART IDENTITY CASCADE;
TRUNCATE TABLE regions RESTART IDENTITY CASCADE;

-- =========================================================
-- REGIONS (UNIQUE name)
-- =========================================================

INSERT INTO regions(name)
SELECT 'R' || gs
FROM generate_series(1,20) gs;

-- =========================================================
-- ORGANIZATIONS (UNIQUE name)
-- =========================================================

INSERT INTO organizations(name,address)
SELECT
    'Organization ' || gs,
    'Address ' || gs
FROM generate_series(1,500) gs;

-- =========================================================
-- ORG UNITS
-- 10 per organization = 5000
-- =========================================================

INSERT INTO organization_units(org_id, region_id, name, address)
SELECT
    o.org_id,
    ((o.org_id - 1) % 20) + 1,
    'Unit ' || u,
    'Address Org ' || o.org_id || ' Unit ' || u
FROM organizations o
CROSS JOIN generate_series(1,10) u;

-- =========================================================
-- USERS (500K) UNIQUE email
-- =========================================================

INSERT INTO users(
    org_unit_id,
    name,
    email,
    password_hash,
    contact,
    country,
    is_active
)
SELECT
    ((gs - 1) % 5000) + 1,
    'User ' || gs,
    'user' || gs || '@mail.com',
    md5(gs::text),
    '9999999999',
    'India',
    (random() > 0.05)
FROM generate_series(1,500000) gs;

-- =========================================================
-- TEAMS
-- UNIQUE(org_unit_id, name)
-- 5 per org unit = 25K
-- =========================================================

INSERT INTO teams(org_unit_id,name)
SELECT
    ou.org_unit_id,
    'Team ' || t
FROM organization_units ou
CROSS JOIN generate_series(1,5) t;

-- =========================================================
-- USER_TEAMS
-- 1 mapping/user
-- =========================================================

INSERT INTO user_teams(user_id, team_id)
SELECT
    u.user_id,
    ((row_number() OVER()) % 25000) + 1
FROM users u;

-- =========================================================
-- PERMISSIONS (UNIQUE)
-- =========================================================

INSERT INTO permissions(name)
VALUES
('create'),
('read'),
('update'),
('delete'),
('approve'),
('execute');

-- =========================================================
-- ROLES UNIQUE(org_id,name)
-- 5 per org = 2500
-- =========================================================

INSERT INTO roles(org_id,name)
SELECT
    o.org_id,
    r.role_name
FROM organizations o
CROSS JOIN (
    VALUES
    ('Admin'),
    ('Manager'),
    ('Reviewer'),
    ('Operator'),
    ('Viewer')
) AS r(role_name);

-- =========================================================
-- ROLE PERMISSIONS UNIQUE(role_id, permission_id)
-- =========================================================

INSERT INTO role_permissions(role_id, permission_id)
SELECT
    r.id,
    p.id
FROM roles r
CROSS JOIN permissions p;

-- =========================================================
-- USER_ROLES UNIQUE(user_id, role_id)
-- One role per user
-- =========================================================

INSERT INTO user_roles(user_id, role_id)
SELECT
    u.user_id,
    ((row_number() OVER()) % 2500) + 1
FROM users u;

-- =========================================================
-- WORKFLOWS (200K)
-- =========================================================

INSERT INTO workflows(
    org_id,
    org_unit_id,
    name,
    is_active,
    created_by
)
SELECT
    ((gs - 1) % 500) + 1,
    ((gs - 1) % 5000) + 1,
    'Workflow ' || gs,
    (random() > 0.2),
    (
        SELECT user_id
        FROM users
        OFFSET ((gs - 1) % 500000)
        LIMIT 1
    )
FROM generate_series(1,200000) gs;

-- =========================================================
-- WORKFLOW STEPS
-- UNIQUE(workflow_id, step_number)
-- 5 steps each = 1M
-- =========================================================

INSERT INTO workflow_steps(
    workflow_id,
    step_number,
    step_name,
    step_config
)
SELECT
    w.id,
    s.step_no,
    'Step ' || s.step_no,
    jsonb_build_object(
        'retry', 3,
        'timeout', 30,
        'notify', true
    )
FROM workflows w
CROSS JOIN (
    VALUES (1),(2),(3),(4),(5)
) s(step_no);

-- -- =========================================================
-- -- WORKFLOW REGIONS
-- -- =========================================================

INSERT INTO workflow_regions(workflow_id, region_id)
SELECT
    id,
    ((id - 1) % 20) + 1
FROM workflows;

-- -- =========================================================
-- -- WORKFLOW RUNS (5 MILLION)
-- -- UNIQUE idempotency_key
-- -- =========================================================

INSERT INTO workflow_runs(
    workflow_id,
    idempotency_key,
    status,
    started_at,
    completed_at,
    trigger_type,
    triggered_by_user_id,
    trigger_metadata
)
SELECT
    ((gs - 1) % 200000) + 1,
    'idem_' || gs,
    (
        ARRAY[
            'pending',
            'active',
            'failed',
            'cancelled',
            'completed'
        ]
    )[ ((gs - 1) % 5) + 1 ]::workflow_status,
    now() - ((gs % 730) || ' days')::interval,
    now() - (((gs % 730) - 1) || ' days')::interval,
    (
        ARRAY['manual','api','cron']
    )[ ((gs - 1) % 3) + 1 ],
    (
        SELECT user_id
        FROM users
        OFFSET ((gs - 1) % 500000)
        LIMIT 1
    ),
    jsonb_build_object(
        'request_id', gs,
        'source', 'benchmark'
    )
FROM generate_series(1,5000000) gs;

-- =========================================================
-- WORKFLOW LOGS (15 MILLION)
-- =========================================================

INSERT INTO workflow_logs(
    workflow_run_id,
    workflow_step_id,
    status,
    log
)
SELECT
    ((gs - 1) % 5000000) + 1,
    ((gs - 1) % 1000000) + 1,
    (
        ARRAY['ok','fail','retry']
    )[ ((gs - 1) % 3) + 1 ],
    'Execution log #' || gs
FROM generate_series(1,15000000) gs;
