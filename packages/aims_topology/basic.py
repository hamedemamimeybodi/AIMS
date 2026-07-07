from __future__ import annotations


def has_duplicate_vertices(vertices: list[list[float]]) -> bool:
    seen = set()
    for vertex in vertices:
        key = tuple(round(float(v), 9) for v in vertex[:2])
        if key in seen:
            return True
        seen.add(key)
    return False
