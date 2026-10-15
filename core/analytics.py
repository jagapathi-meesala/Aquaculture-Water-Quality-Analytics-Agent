from __future__ import annotations
from datetime import datetime
from typing import Any
REQUIRED = ("pond_id", "timestamp", "parameter", "value", "unit")

def _finding(code: str, severity: str, message: str, **evidence: Any) -> dict[str, Any]:
    return {"code": code, "severity": severity, "message": message, "evidence": evidence}

def analyze(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict): raise ValueError("Input must be a JSON object.")
    observations=data.get("observations", [])
    thresholds=data.get("thresholds", {})
    if not isinstance(observations,list): raise ValueError("observations must be a list.")
    if not isinstance(thresholds,dict): raise ValueError("thresholds must be an object.")
    findings=[]; valid=[]; seen=set()
    for i,row in enumerate(observations):
        if not isinstance(row,dict):
            findings.append(_finding("INVALID_ROW","high","Observation must be an object.",row_index=i)); continue
        missing=[k for k in REQUIRED if row.get(k) is None or row.get(k)==""]
        if missing:
            findings.append(_finding("MISSING_FIELDS","medium","Observation is missing required fields.",row_index=i,fields=missing)); continue
        try: value=float(row["value"])
        except (TypeError,ValueError):
            findings.append(_finding("NON_NUMERIC_VALUE","high","Measurement value is not numeric.",row_index=i,value=row.get("value"))); continue
        if not (value == value and abs(value) != float("inf")):
            findings.append(_finding("NON_FINITE_VALUE","high","Measurement must be finite.",row_index=i,value=row.get("value"))); continue
        try: ts=datetime.fromisoformat(str(row["timestamp"]).replace("Z","+00:00"))
        except ValueError:
            findings.append(_finding("INVALID_TIMESTAMP","medium","Timestamp is not parseable as ISO format.",row_index=i,timestamp=row["timestamp"])); continue
        key=(str(row["pond_id"]),str(row["timestamp"]),str(row["parameter"]))
        if key in seen: findings.append(_finding("DUPLICATE_OBSERVATION","medium","Duplicate pond/timestamp/parameter record.",row_index=i,key=list(key)))
        seen.add(key)
        item={**row,"_value":value,"_time":ts,"_index":i}; valid.append(item)
        lim=thresholds.get(str(row["parameter"]))
        if lim is not None:
            if not isinstance(lim,dict):
                findings.append(_finding("INVALID_THRESHOLD","high","Threshold must be an object with optional min/max.",parameter=row["parameter"])); continue
            try:
                lo=float(lim["min"]) if lim.get("min") is not None else None
                hi=float(lim["max"]) if lim.get("max") is not None else None
            except (TypeError,ValueError):
                findings.append(_finding("INVALID_THRESHOLD","high","Threshold bounds must be numeric.",parameter=row["parameter"])); continue
            if lo is not None and value < lo: findings.append(_finding("BELOW_CONFIGURED_MIN","high","Measurement is below the configured minimum.",row_index=i,parameter=row["parameter"],value=value,unit=row["unit"],minimum=lo))
            if hi is not None and value > hi: findings.append(_finding("ABOVE_CONFIGURED_MAX","high","Measurement is above the configured maximum.",row_index=i,parameter=row["parameter"],value=value,unit=row["unit"],maximum=hi))
    groups={}
    for r in valid: groups.setdefault((str(r["pond_id"]),str(r["parameter"])),[]).append(r)
    trends=[]
    for (pond,param),rows in sorted(groups.items()):
        rows=sorted(rows,key=lambda x:x["_time"])
        first,last=rows[0],rows[-1]; delta=last["_value"]-first["_value"]
        pct=(delta/abs(first["_value"])*100) if first["_value"] != 0 else None
        trends.append({"pond_id":pond,"parameter":param,"unit":last["unit"],"observations":len(rows),"first_value":first["_value"],"first_timestamp":first["timestamp"],"last_value":last["_value"],"last_timestamp":last["timestamp"],"change":round(delta,4),"percent_change":round(pct,2) if pct is not None else None,"interpretation":"descriptive change only; not a forecast"})
    suggestions=[]
    codes={f["code"] for f in findings}
    if codes & {"ABOVE_CONFIGURED_MAX","BELOW_CONFIGURED_MIN"}: suggestions.append("Verify the reading with an appropriate calibrated instrument and follow site escalation procedures.")
    if codes & {"MISSING_FIELDS","INVALID_TIMESTAMP","NON_NUMERIC_VALUE","NON_FINITE_VALUE","DUPLICATE_OBSERVATION"}: suggestions.append("Resolve data-quality issues before using the affected observations for operational decisions.")
    if not thresholds: suggestions.append("No thresholds were supplied; results cannot be classified against operating limits.")
    if not suggestions: suggestions.append("Review trends alongside species, life stage, stocking density, feeding, weather, and system context.")
    return {"agent":"aquaculture-water-quality-analytics-agent","summary":{"observations_received":len(observations),"valid_observations":len(valid),"findings":len(findings),"parameters_with_trends":len(trends)},"findings":findings,"trends":trends,"recommendations":suggestions,"limitations":["Thresholds are user-supplied and must be appropriate for the culture context.","Trend deltas are descriptive and do not predict future water quality.","No sensor calibration, laboratory confirmation, or live system integration is performed.","This tool does not prescribe dosing or control equipment."]}
