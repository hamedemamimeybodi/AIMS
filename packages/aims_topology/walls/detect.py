from collections import Counter
import ezdxf


class WallDetector:

    def __init__(self, filename):
        self.doc = ezdxf.readfile(filename)
        self.msp = self.doc.modelspace()

    def detect(self):

        walls = []

        for entity in self.msp:

            if entity.dxftype() != "LINE":
                continue

            layer = entity.dxf.layer.lower()

            if layer in ("door", "win", "dim", "text", "view"):
                continue

            start = entity.dxf.start
            end = entity.dxf.end

            walls.append(
                {
                    "layer": layer,
                    "start": (start.x, start.y),
                    "end": (end.x, end.y),
                }
            )

        return walls


if __name__ == "__main__":

    detector = WallDetector("examples/RP-0001/floor 1-3.dxf")

    walls = detector.detect()

    print(f"Detected Walls : {len(walls)}")

    c = Counter(w["layer"] for w in walls)

    print()

    for k, v in c.items():
        print(f"{k:20} {v}")