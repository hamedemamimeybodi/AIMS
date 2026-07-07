from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from packages.aims_geometry.adf import ADFDocument

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adf_version TEXT NOT NULL,
    source_path TEXT NOT NULL,
    entity_count INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS layers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    adf_entity_id INTEGER NOT NULL,
    entity_type TEXT NOT NULL,
    layer TEXT NOT NULL,
    geometry_json TEXT NOT NULL,
    text_value TEXT,
    attributes_json TEXT NOT NULL,
    FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS validation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    rule_code TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    entity_id INTEGER,
    FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
);
"""


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_SQL)


def write_adf_to_sqlite(adf: ADFDocument, db_path: str | Path) -> int:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(path) as connection:
        initialize_database(connection)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO documents (adf_version, source_path, entity_count) VALUES (?, ?, ?)",
            (adf.version, adf.source_path, adf.entity_count),
        )
        document_id = int(cursor.lastrowid)

        cursor.executemany(
            "INSERT INTO layers (document_id, name) VALUES (?, ?)",
            [(document_id, layer) for layer in adf.layers],
        )

        cursor.executemany(
            """
            INSERT INTO entities (
                document_id, adf_entity_id, entity_type, layer,
                geometry_json, text_value, attributes_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    document_id,
                    entity.entity_id,
                    entity.entity_type,
                    entity.layer,
                    json.dumps(entity.geometry, ensure_ascii=False),
                    entity.text,
                    json.dumps(entity.attributes, ensure_ascii=False),
                )
                for entity in adf.entities
            ],
        )
        connection.commit()
        return document_id
