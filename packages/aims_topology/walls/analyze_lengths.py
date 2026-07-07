import math
import ezdxf

doc = ezdxf.readfile("examples/RP-0001/floor 1-3.dxf")
msp = doc.modelspace()

lengths = []

for e in msp:
    if e.dxftype() != "LINE":
        continue

    layer = e.dxf.layer.lower()

    if layer in ("door", "win", "dim", "text", "view"):
        continue

    s = e.dxf.start
    t = e.dxf.end

    length = math.hypot(t.x - s.x, t.y - s.y)

    lengths.append((layer, round(length, 2)))

lengths.sort(key=lambda x: x[1], reverse=True)

print("Longest 50 lines\n")

for layer, length in lengths[:50]:
    print(f"{layer:15} {length:10.2f}")