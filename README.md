# Aquaculture Water Quality Analytics Agent

An explainable screening tool for supplied aquaculture water-quality measurements. It validates observations, compares values with user-provided thresholds, summarizes recent trends, and drafts conservative follow-up checks.

## Features
- Validate required fields, units, timestamps, and numeric values.
- Flag observations outside configured parameter ranges.
- Compare first and last observations for each parameter when a time series is supplied.
- Generate JSON findings with evidence and review recommendations.

## Run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python verification/readiness_audit.py
python -m core.cli examples/water_quality_case.json --output report.json
```

Input values and thresholds must be appropriate for the species, life stage, culture system, and local conditions. This tool is not a substitute for calibrated instruments, laboratory confirmation, or qualified aquaculture advice. It does not control pumps, aerators, dosing, or other equipment.
