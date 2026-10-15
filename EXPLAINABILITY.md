# Explainability

## Inputs
Each observation should include pond/tank identifier, timestamp, parameter name, numeric value, and unit. Thresholds are optional and must be supplied by the operator for the relevant culture context.

## Decision
The analyzer validates records, checks values against provided bounds, and compares chronological first/last values per parameter. Trend calculations are descriptive only.

## Limits
It does not establish biological causation, infer unprovided limits, validate sensor calibration, or control equipment. Species, life stage, salinity, temperature, system type, and local operating guidance can materially change interpretation.

## Tool: validate-water-quality-data
### Inputs and Data Sources
Supplied observation records and optional threshold configuration.
### Decision and Reasoning
Checks required fields, numeric values, units, and duplicate records.
### Outputs and Evidence
Validation findings with row index and field/value evidence.
### Limits and Constraints
No external lab or sensor data is retrieved.
### Failure Handling
Malformed input raises a clear validation error; individual bad rows are reported.
### Human Review
Confirm units, timestamps, sensor calibration, and sample identity.

## Tool: analyze-water-quality-trends
### Inputs and Data Sources
Valid observations with timestamps and parameter names.
### Decision and Reasoning
Sorts observations and compares earliest/latest values per parameter.
### Outputs and Evidence
Change and percent change where mathematically defined.
### Limits and Constraints
Two-point change is not a predictive forecast.
### Failure Handling
Percent change is omitted when the baseline is zero or unavailable.
### Human Review
Review sampling frequency and environmental context.

## Tool: draft-response-guidance
### Inputs and Data Sources
Threshold findings and data-quality findings.
### Decision and Reasoning
Maps finding types to conservative inspection suggestions.
### Outputs and Evidence
Review recommendations tied to finding codes.
### Limits and Constraints
Does not prescribe treatment, chemical dose, or equipment setpoint.
### Failure Handling
Unknown parameters receive a generic verify-and-review suggestion.
### Human Review
Follow site procedures and consult qualified aquaculture personnel.
