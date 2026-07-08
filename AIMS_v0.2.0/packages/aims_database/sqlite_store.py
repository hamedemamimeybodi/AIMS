from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from packages.aims_core.adf import ADFDocument
from packages.aims_database.schema import SCHEMA_SQL


def write_sqlite(document: ADFDocument, db_path: str | Path) -> Path:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        conn.execute("DELETE FROM entities WHERE source_file = ?", (document.source_file,))
        for entity in document.entities:
            conn.execute(
                """
                INSERT OR REPLACE INTO entities (
                    id, source_file, source, handle, entity_type, layer, category, bim_class,
                    geometry_type, geometry_json, text, properties_json, issues_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entity.id,
                    document.source_file,
                    entity.source,
                    entity.handle,
                    entity.entity_type,
                    entity.layer,
                    entity.category.value,
                    entity.bim_class,
                    entity.geometry.type if entity.geometry else None,
                    entity.geometry.model_dump_json() if entity.geometry else None,
                    entity.text,
                    json.dumps(entity.properties, ensure_ascii=False),
                    json.dumps([i.model_dump() for i in entity.issues], ensure_ascii=False),
                ),
            )
        conn.execute(
            "INSERT INTO audit_summary (source_file, total_entities, total_issues) VALUES (?, ?, ?)",
            (document.source_file, len(document.entities), document.issue_count()),
        )
        conn.commit()
    return db_path
