from collections import Counter
from pathlib import Path
import ezdxf

DXF_FILE = Path("examples/RP-0001/floor 1-3.dxf")

def main():
    doc = ezdxf.readfile(DXF_FILE)
    msp = doc.modelspace()

    entities = Counter()
    layers = Counter()

    for e in msp:
        entities[e.dxftype()] += 1
        layers[e.dxf.layer] += 1

    print("AIMS DXF REPORT")
    print("=" * 40)
    print("File:", DXF_FILE)
    print("DXF Version:", doc.dxfversion)
    print("Units:", doc.header.get("$INSUNITS", "Unknown"))
    print("Layers:", len(layers))
    print("Blocks:", len(doc.blocks))
    print("Entities:", sum(entities.values()))

    print("\nEntity Types")
    print("-" * 40)
    for k, v in entities.most_common():
        print(f"{k:20} {v}")

    print("\nLayers")
    print("-" * 40)
    for k, v in layers.most_common():
        print(f"{k:30} {v}")

if __name__ == "__main__":
    main()