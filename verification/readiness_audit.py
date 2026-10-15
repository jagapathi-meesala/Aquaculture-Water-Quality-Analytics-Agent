from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=['agent.yaml','SOUL.md','RULES.md','DUTIES.md','AGENTS.md','EXPLAINABILITY.md','README.md','requirements.txt','core/analytics.py','core/cli.py','tests/test_analytics.py','examples/water_quality_case.json','tools/validate-water-quality-data.yaml','tools/analyze-water-quality-trends.yaml','tools/draft-response-guidance.yaml','skills/water-quality-review/SKILL.md','skills/trend-analysis/SKILL.md','skills/response-planning/SKILL.md']
missing=[p for p in REQUIRED if not (ROOT/p).is_file()]
manifest=yaml.safe_load((ROOT/'agent.yaml').read_text())
if manifest.get('name')!='aquaculture-water-quality-analytics-agent': missing.append('agent.yaml name mismatch')
print(f'PASS: {len(REQUIRED)-len([p for p in REQUIRED if not (ROOT/p).is_file()])}/{len(REQUIRED)} required files present')
if missing: print('FAIL:',missing); raise SystemExit(1)
print('PASS: manifest name and required structure')
