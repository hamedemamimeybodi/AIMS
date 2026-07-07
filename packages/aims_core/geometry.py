from __future__ import annotations

import math


def distance(a: list[float], b: list[float]) -> float:
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])
    return math.hypot(ax - bx, ay - by)


def polyline_length(vertices: list[list[float]]) -> float:
    if len(vertices) < 2:
        return 0.0
    return sum(distance(vertices[i], vertices[i + 1]) for i in range(len(vertices) - 1))


def polygon_area(vertices: list[list[float]]) -> float:
    if len(vertices) < 3:
        return 0.0
    area = 0.0
    pts = vertices[:]
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    for i in range(len(pts) - 1):
        area += float(pts[i][0]) * float(pts[i + 1][1])
        area -= float(pts[i + 1][0]) * float(pts[i][1])
    return abs(area) / 2.0
