from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from packages.aims_domain import ADFDocument
from packages.aims_validator.engine import ValidationReport

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adf_version TEXT NOT NULL,
    source_path TEXT NOT NULL,
    feature_count INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS layers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY(document_id) REFERENCES documents(id)
);

CREATE TABLE IF NOT EXISTS features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    feature_id TEXT NOT NULL,
    source_entity TEXT NOT NULL,
    layer TEXT NOT NULL,
    geometry_json TEXT NOT NULL,
    attributes_json TEXT NOT NULL,
    text_value TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
);

CREATE TABLE IF NOT EXISTS validation_issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    rule_id TEXT NOT NULL,
    severity TEXT NOT NULL,
    feature_id TEXT,
    message TEXT NOT NULL,
    why_it_matters TEXT,
    suggested_fix TEXT,
    FOREIGN KEY(document_id) REFERENCES documents(id)
);
"""


def initialize(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)


def save_document(adf: ADFDocument, report: ValidationReport, db_path: str | Path) -> int:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        initialize(conn)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO documents (adf_version, source_path, feature_count) VALUES (?, ?, ?)",
            (adf.adf_version, adf.source_path, adf.feature_count),
        )
        document_id = int(cur.lastrowid)

        cur.executemany(
            "INSERT INTO layers (document_id, name) VALUES (?, ?)",
            [(document_id, layer) for layer in adf.layers],
        )

        cur.executemany(
            """
            INSERT INTO features
            (document_id, feature_id, source_entity, layer, geometry_json, attributes_json, text_value)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    document_id,
                    f.feature_id,
                    f.source_entity,
                    f.layer,
                    json.dumps({
                        "type": f.geometry.type,
                        "coordinates": f.geometry.coordinates,
                        "properties": f.geometry.properties,
                    }, ensure_ascii=False),
                    json.dumps(f.attributes, ensure_ascii=False),
                    f.text,
                )
                for f in adf.features
            ],
        )

        cur.executemany(
            """
            INSERT INTO validation_issues
            (document_id, rule_id, severity, feature_id, message, why_it_matters, suggested_fix)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    document_id,
                    i.rule_id,
                    i.severity,
                    i.feature_id,
                    i.message,
                    i.why_it_matters,
                    i.suggested_fix,
                )
                for i in report.issues
            ],
        )

        conn.commit()
        return document_id
