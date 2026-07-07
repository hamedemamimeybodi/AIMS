import math
from collections import Counter
import ezdxf

doc = ezdxf.readfile("examples/RP-0001/floor 1-3.dxf")
msp = doc.modelspace()

angles = Counter()

for e in msp:
    if e.dxftype() != "LINE":
        continue

    if e.dxf.layer.lower() in ("door","win","dim","text","view"):
        continue

    s = e.dxf.start
    t = e.dxf.end

    angle = math.degrees(math.atan2(t.y-s.y, t.x-s.x))

    angle = round(angle)

    if angle < 0:
        angle += 180

    angles[angle] += 1

print("Angle Histogram")
print("----------------")

for a,c in sorted(angles.items()):
    print(f"{a:3d}° : {c}")