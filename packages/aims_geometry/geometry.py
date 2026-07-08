from __future__ import annotations

from math import hypot
from typing import Iterable, List, Sequence, Tuple

Point = Sequence[float]


def distance(a: Point, b: Point) -> float:
    return hypot(float(a[0]) - float(b[0]), float(a[1]) - float(b[1]))


def polyline_length(points: Iterable[Point], closed: bool = False) -> float:
    pts = list(points)
    if len(pts) < 2:
        return 0.0
    total = sum(distance(a, b) for a, b in zip(pts, pts[1:]))
    if closed:
        total += distance(pts[-1], pts[0])
    return total


def polygon_area(points: Iterable[Point]) -> float:
    pts = list(points)
    if len(pts) < 3:
        return 0.0
    area = 0.0
    for a, b in zip(pts, pts[1:] + pts[:1]):
        area += float(a[0]) * float(b[1]) - float(b[0]) * float(a[1])
    return abs(area) / 2.0


def bbox(points: Iterable[Point]) -> Tuple[float, float, float, float] | None:
    pts = list(points)
    if not pts:
        return None
    xs = [float(p[0]) for p in pts]
    ys = [float(p[1]) for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def geometry_signature(points: List[List[float]], precision: int = 4) -> tuple:
    return tuple((round(float(p[0]), precision), round(float(p[1]), precision), round(float(p[2] if len(p) > 2 else 0.0), precision)) for p in points)
