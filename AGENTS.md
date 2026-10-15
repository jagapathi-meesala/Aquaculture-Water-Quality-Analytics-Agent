# Agent Operating Guide
Accept JSON observations containing `pond_id`, `timestamp`, `parameter`, `value`, and `unit`, with optional `thresholds` mapping parameter names to `min`/`max`. Report malformed rows rather than guessing. Output a summary, findings, trends, and limitations. No external integrations or actuation are performed.
