from __future__ import annotations

import time
from pathlib import Path

from packages.aims_parser import parse_dxf


def main() -> None:
    path = Path("examples/simple_site.dxf")
    start = time.perf_counter()
    adf = parse_dxf(path)
    elapsed = time.perf_counter() - start
    print({"features": adf.feature_count, "seconds": elapsed})


if __name__ == "__main__":
    main()
