# Fraud triage — rolling 72h (Pacific Time)

Generates the daily compliance fraud-triage report for members with confirmed IAPs ≥ $19.99 USD whose exact linked bonus multiplier is &lt; 1.0×.

## Run

```bash
# Expects cohort extracts under /tmp/report_data/ (purchases, profiles, verisoul, payout_risk, earnings).
python3 reports/fraud_triage/generate_report.py
```

Outputs:
- `reports/fraud_triage/output/fraud_triage_72h.html` — full report
- `reports/fraud_triage/output/summary.json` — headline metrics
- Charts (PNG) alongside the HTML
- Copies under `/opt/cursor/artifacts/` when that path exists

## Definitions

See the Methodology section inside the HTML report and `REPORT.md` for the run snapshot.

Allowlist titles are fixed (Pixel Flow, Animals & Coins, and the full Richard/Rex non-cash list). Do not infer membership from in-window revenue.
