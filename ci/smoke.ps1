$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest
pytest -q
python -m aims.cli validate
python -m aims.cli audit examples/simple_site.dxf --sqlite reports/smoke.sqlite --geojson reports/smoke.geojson --ifc reports/smoke.ifc --out reports/smoke.md --html reports/smoke.html --json-report reports/smoke.json
