import pytest
from core.analytics import analyze

def sample():
 return {"thresholds":{"dissolved_oxygen":{"min":5,"max":12}},"observations":[{"pond_id":"P1","timestamp":"2026-10-14T08:00:00","parameter":"dissolved_oxygen","value":6,"unit":"mg/L"},{"pond_id":"P1","timestamp":"2026-10-14T09:00:00","parameter":"dissolved_oxygen","value":4,"unit":"mg/L"}]}

def test_flags_below_minimum():
 r=analyze(sample()); assert any(f["code"]=="BELOW_CONFIGURED_MIN" for f in r["findings"])
def test_trend_delta():
 r=analyze(sample()); assert r["trends"][0]["change"]==-2

def test_no_threshold_disclaimer():
 r=analyze({"observations":[]}); assert any("No thresholds" in x for x in r["recommendations"])
def test_invalid_row_reported():
 r=analyze({"observations":["bad"]}); assert r["findings"][0]["code"]=="INVALID_ROW"
def test_missing_fields_reported():
 r=analyze({"observations":[{"pond_id":"P1"}]}); assert r["findings"][0]["code"]=="MISSING_FIELDS"
def test_duplicate_record_reported():
 row={"pond_id":"P1","timestamp":"2026-10-14T08:00:00","parameter":"pH","value":7,"unit":"pH"}
 r=analyze({"observations":[row,row]}); assert any(f["code"]=="DUPLICATE_OBSERVATION" for f in r["findings"])
def test_invalid_input_raises():
 with pytest.raises(ValueError): analyze([])
def test_threshold_upper_bound():
 d=sample(); d["observations"][1]["value"]=14
 r=analyze(d); assert any(f["code"]=="ABOVE_CONFIGURED_MAX" for f in r["findings"])
