# Install AIMS

## Requirements

- Python 3.11 or newer
- Git
- Optional: GitHub Actions for CI

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Verify

```bash
python -m aims.cli validate --version 1.0.0
python -m aims.cli release-check --version 1.0.0
pytest
```
