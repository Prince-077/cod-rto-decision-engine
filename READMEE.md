# COD RTO Decision Engine

**AI-Assisted Cash-on-Delivery Risk Analysis and Decision Support**

## Overview

The COD RTO Decision Engine analyses historical Cash-on-Delivery (COD) orders to identify potential Return to Origin (RTO) risks and recommend suitable actions.

The system uses configurable business rules based on customer history, address quality and historical pincode RTO patterns. It also generates mock WhatsApp messages and provides a Streamlit dashboard for reviewing decisions and estimated financial impact.

The goal is to reduce avoidable RTO costs without creating unnecessary friction for genuine customers.

## Features

- Customer history-based risk rules.
- Address and customer-name quality checks.
- Pincode-level historical RTO analysis.
- Configurable thresholds in `config.py`.
- Four decision categories:
  - `SHIP_AS_IS`
  - `WHATSAPP_CONFIRMATION`
  - `PREPAID_NUDGE`
  - `HOLD_MANUAL_REVIEW`
- Mock WhatsApp message generation.
- Chronological train/test split for initial backtesting.
- Streamlit dashboard for decision and RTO metrics.
- Illustrative financial impact calculations.

## Technology Stack

- Python
- pandas
- Streamlit
- uv

## Project Structure

```text
soft/
├── src/
├── .gitignore
├── .python-version
├── analyze_data.py
├── backtest.py
├── backtest_results.csv
├── config.py
├── dashboard.py
├── decision_engine.py
├── founder_memo.md
├── inspect_data.py
├── last.py
├── main.py
├── order_decisions_demo.csv
├── order_decisions_with_messages.csv
├── orders_sample.csv
├── pincode_risk_report.csv
├── pyproject.toml
├── README.md
├── test_decision.py
└── uv.lock
```

Generated CSV reports are outputs created by the scripts. The `.venv` directory, if present, should not be committed to GitHub.

## Prerequisites

- Python
- uv installed and available in the terminal
- The provided `orders_sample.csv` file in the project root

## Installation

Open PowerShell in the project directory.

### 1. Install dependencies

```powershell
uv add pandas streamlit
```

### 2. Analyse the dataset

```powershell
uv run python analyze_data.py
```

This generates `pincode_risk_report.csv`.

### 3. Run the historical backtest

```powershell
uv run python backtest.py
```

This generates `backtest_results.csv`.

### 4. Generate order decisions and mock messages

```powershell
uv run python main.py
```

This generates `order_decisions_with_messages.csv`.

### 5. Launch the dashboard

```powershell
uv run streamlit run dashboard.py
```

Open the local URL shown in the terminal to view the dashboard.

## Decision Policy

| Risk signal | Recommended action |
|---|---|
| No strong risk signal | Ship as-is |
| Incomplete or questionable address/name | WhatsApp confirmation |
| Previous RTO history | Prepaid nudge |
| Multiple previous RTOs combined with elevated pincode risk | Manual review |

The thresholds can be adjusted in `config.py`.

These rules are a baseline decision policy and should be validated before production use. A single missing field or unusual name should not be treated as proof of fraud.

## Dashboard

The Streamlit dashboard includes:

- Daily order count.
- Observed RTO order count and RTO rate.
- Decision-bucket counts.
- Action-wise outcomes on the test dataset.
- Editable assumptions for RTO cost and intervention cost.
- An illustrative financial impact scenario.
- A downloadable CSV of test results.

If the dataset does not include yesterday's orders, the dashboard displays the latest available date.

## Backtesting

The initial backtest sorts completed orders by `order_datetime`, uses an earlier portion of the dataset as historical training data, and evaluates decisions on a later test portion.

Pincode RTO rates are calculated from the historical training portion and applied to test orders.

This is an initial evaluation, not proof that an intervention causes RTO reduction. Customer-history fields must also be checked to ensure they were available at the time each order decision would have been made.

## Financial Impact

The dashboard allows users to adjust:

- Estimated cost per RTO.
- Cost per intervention.
- Assumed RTO reduction for targeted orders.

The resulting numbers are **illustrative estimates, not verified savings**. Actual impact requires measured intervention effectiveness, validated cost assumptions and a suitable comparison group.

## WhatsApp Mock

The WhatsApp component generates sample messages for the recommended actions. It does not send real WhatsApp messages or connect to the WhatsApp Business API.

## Limitations

- Small pincode samples can produce unreliable risk estimates.
- Missing or unusual customer data can lead to false positives.
- Duplicate order IDs require investigation before removing records.
- Historical associations do not prove that interventions will prevent RTO.
- Financial estimates depend on assumptions.
- The current decision policy is rule-based; an LLM integration should be treated as a separate, validated component.

## Two-Week Rollout Plan

### Week 1 — Validation

- Audit missing values and duplicate records.
- Verify that risk features were available at decision time.
- Review high-risk decisions with operations staff.
- Validate costs and intervention assumptions.
- Test message templates in mock mode.

### Week 2 — Controlled Pilot

- Run a small pilot with eligible orders.
- Compare outcomes against an appropriate baseline or comparison group.
- Track RTO rate, delivery success, conversion, intervention costs and customer complaints.
- Review false positives and tune thresholds.
- Expand only if measured results justify the added customer friction.

## Success Metrics

- Overall RTO rate.
- RTO rate by decision bucket.
- Delivery success rate.
- Intervention cost.
- Conversion and cancellation rates.
- False-positive rate.
- Net financial impact based on actual costs and measured outcomes.

## Project Status

**Prototype — ready for further validation.**

The project demonstrates data analysis, configurable decision rules, historical backtesting, mock messaging and dashboard reporting. Production deployment requires additional validation and a controlled intervention pilot.

## Author

**Prince Kumar**

Associate Software Engineer / AI Automation Engineer Assignment