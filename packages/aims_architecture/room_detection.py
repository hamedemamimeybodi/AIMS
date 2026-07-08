from __future__ import annotations

from typing import List

from packages.aims_core.adf import ADFCategory, ADFDocument, ADFEntity


def room_candidates(document: ADFDocument) -> List[ADFEntity]:
    """Return room-like closed polylines. Full spatial room detection is a later milestone."""
    return [
        entity for entity in document.entities
        if entity.category == ADFCategory.ROOM
        and entity.geometry is not None
        and entity.geometry.type == "polyline"
        and entity.geometry.closed
    ]
