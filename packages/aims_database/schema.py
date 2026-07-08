SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    source_file TEXT NOT NULL,
    source TEXT NOT NULL,
    handle TEXT,
    entity_type TEXT NOT NULL,
    layer TEXT NOT NULL,
    category TEXT NOT NULL,
    bim_class TEXT,
    geometry_type TEXT,
    geometry_json TEXT,
    text TEXT,
    properties_json TEXT NOT NULL,
    issues_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    total_entities INTEGER NOT NULL,
    total_issues INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""
