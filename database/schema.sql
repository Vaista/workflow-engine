-- \c workflow_engine

CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE TYPE workflow_status AS ENUM ('pending', 'active', 'failed', 'cancelled', 'completed');

CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY not null,
    name varchar(60) UNIQUE not null,
    code varchar(10) UNIQUE not null
);

CREATE TABLE organizations (
    org_id SERIAL PRIMARY KEY not null,
    name varchar(40) UNIQUE not null,
    address varchar(60)
);

CREATE TABLE organization_units (
    org_unit_id SERIAL PRIMARY KEY not null,
    org_id int REFERENCES organizations(org_id),
    region_id int REFERENCES regions(region_id),
    name varchar(40) NOT NULL,
    address varchar(120) NOT NULL,
    CONSTRAINT uq_org_unit_org_id_name UNIQUE (org_id, name)
);

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id int REFERENCES organizations(id),
    org_unit_id int REFERENCES organization_units(org_unit_id),
    name varchar(60) not null,
    email TEXT UNIQUE NOT NULL,
    password_hash varchar(255) not null,
    contact varchar(20),
    country varchar(20),
    is_active boolean DEFAULT true,
    created_on timestamp DEFAULT current_timestamp
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY not null,
    org_unit_id int REFERENCES organization_units(org_unit_id),
    name varchar(30),
    UNIQUE(org_unit_id, name)
);

CREATE TABLE user_teams (
    id SERIAL PRIMARY KEY not null,
    user_id UUID REFERENCES users(user_id),
    team_id int REFERENCES teams(id)
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY NOT NULL,
    org_id int REFERENCES organizations(org_id),
    name varchar(20) not null,
    UNIQUE(org_id, name)
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY NOT NULL,
    name varchar(20) UNIQUE NOT NULL
);

CREATE TABLE role_permissions(
    id SERIAL PRIMARY KEY NOT NULL,
    role_id int REFERENCES roles(id),
    permission_id int REFERENCES permissions(id),
    UNIQUE(role_id, permission_id)
);

CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id UUID REFERENCES users(user_id),
    role_id int REFERENCES roles(id),
    UNIQUE(user_id, role_id)
);

CREATE TABLE workflows (
    id SERIAL PRIMARY KEY NOT NULL,
    org_id int REFERENCES organizations(org_id),
    org_unit_id int REFERENCES organization_units(org_unit_id),
    name varchar(30) not null,
    description varchar(255) DEFAULT NULL,
    is_active BOOLEAN DEFAULT false,
    created_by UUID REFERENCES users(user_id),
    created_on timestamp DEFAULT current_timestamp,
    is_deleted BOOLEAN DEFAULT false,
    deleted_at timestamp,
    deleted_by UUID REFERENCES users(user_id)
);

CREATE TABLE workflow_steps (
    id SERIAL PRIMARY KEY not null,
    workflow_id INT REFERENCES workflows(id),
    step_number INT NOT NULL,
    step_name varchar(30) NOT NULL,
    step_description varchar(255) DEFAULT NULL,
    step_config jsonb,
    CONSTRAINT uq_workflow_step_number UNIQUE (workflow_id, step_number)
);

CREATE TABLE workflow_regions (
    id SERIAL PRIMARY KEY NOT NULL,
    workflow_id INT REFERENCES workflows(id),
    region_id INT REFERENCES regions(region_id)
    CONSTRAINT uq_workflow_region_ids UNIQUE (workflow_id, region_id)
);

CREATE TABLE workflow_runs (
    id SERIAL PRIMARY KEY NOT NULL,
    workflow_id INT REFERENCES workflows(id),
    idempotency_key TEXT UNIQUE,
    status workflow_status,
    started_at timestamp,
    completed_at timestamp,
    trigger_type text,
    triggered_by_user_id UUID REFERENCES users(user_id),
    trigger_metadata jsonb
);

CREATE TABLE workflow_logs (
    id SERIAL PRIMARY KEY NOT NULL,
    workflow_run_id INT REFERENCES workflow_runs(id),
    workflow_step_id INT REFERENCES workflow_steps(id),
    status varchar(10),
    log text,
    execution_timestamp timestamp DEFAULT current_timestamp
);



-- INDEXES

CREATE INDEX idx_org_units_org_region
ON organization_units(org_id, region_id);

CREATE INDEX users_org_unit_id
ON users(org_id, org_unit_id);

CREATE INDEX users_teams_team_id
ON user_teams(team_id);

CREATE INDEX idx_workflows_org_unit_live
ON workflows(org_unit_id, created_on DESC)
WHERE is_deleted = false;

CREATE INDEX idx_workflows_org_live
ON workflows(org_id, created_on DESC)
WHERE is_deleted = false;

CREATE INDEX idx_workflow_region
ON workflow_regions(region_id);

CREATE INDEX idx_workflow_runs_workflow
ON workflow_runs(workflow_id, status, started_at DESC);

CREATE INDEX idx_workflow_log
ON workflow_logs(workflow_run_id, execution_timestamp DESC);
