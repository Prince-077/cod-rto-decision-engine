# COD RTO Decision Engine — Founder Memo

**Date:** 31 October 2026  
**Status:** Prototype and historical analysis

## 1. Executive Summary

The proposed COD RTO Decision Engine uses historical customer behaviour, address quality and pincode-level RTO patterns to recommend one of four actions: ship as-is, request WhatsApp confirmation, send a prepaid nudge, or hold for manual review.

The objective is to reduce avoidable Return to Origin (RTO) costs while protecting genuine customer orders and maintaining a good customer experience.

The current implementation is a rule-based prototype. Its decisions and financial estimates must be validated before production deployment.

## 2. Key Data Findings

**Finding 1 — Overall RTO exposure**

The initial dataset analysis identified 573 RTO orders among 2,017 completed orders, giving an overall RTO rate of approximately 28.4%.

This indicates a meaningful opportunity to investigate delivery failures and improve COD order verification. RTO should not automatically be interpreted as customer fraud or intentional refusal.

**Finding 2 — Previous RTO history is a useful risk signal**

In the initial customer-history analysis:

- Customers with no previous RTO: 509 RTOs among 1,872 orders (27.19%).
- Customers with one previous RTO: 38 RTOs among 111 orders (34.23%).
- Customers with multiple previous RTOs: 26 RTOs among 34 orders (76.47%).

The multiple-previous-RTO segment has a substantially higher observed RTO rate, but it contains only 34 orders. Treat this as a risk signal to validate, not as sufficient evidence to automatically cancel orders.

**Finding 3 — Address and location quality need validation**

Incomplete address details and historical pincode RTO rates can help prioritise verification. However, a missing pincode, unusual name or short address does not prove an order will fail.

Before using these signals, validate data quality, minimum sample sizes and whether each feature was available when the order decision would have been made.

*Note: Verify these counts against the final cleaned dataset before submission. Add the actual action-wise test results from `backtest_results.csv` rather than inventing performance improvements.*

## 3. Proposed Decision Policy

- **Ship as-is:** No strong risk signals; avoid unnecessary friction for reliable orders.
- **WhatsApp confirmation:** Address or name needs clarification, or the order has a credible elevated-risk signal.
- **Prepaid nudge:** Offer an optional prepaid checkout to selected customers with prior RTO history.
- **Hold for manual review:** Reserve for combinations of strong risk signals; do not automatically cancel based on a single feature.

Thresholds should be editable in `config.py` and monitored for false positives.

## 4. Operations vs Marketing Trade-off

Operations benefits from fewer avoidable RTOs and less wasted delivery effort. Marketing and customer experience teams need to protect conversion rates and avoid frustrating genuine customers with unnecessary confirmation messages.

The recommended approach is targeted intervention rather than blanket restrictions on COD. Measure both outcomes: RTO reduction and the impact on conversion, cancellation, customer complaints and delivery success.

## 5. Backtest and Financial Impact

The prototype uses a chronological historical/test split and estimates pincode risk from the historical training period. This is an initial evaluation, not proof that interventions reduce RTO.

The dashboard's financial impact is scenario-based and depends on editable assumptions about RTO cost, intervention cost and intervention effectiveness. It must not be reported as realised savings.

Before relying on the estimates, verify that all risk features are available at decision time and compare the policy with a baseline on an untouched test period.

## 6. Key Failure Modes

- Incorrect or missing customer history.
- Sparse pincode data producing unstable risk estimates.
- Genuine customers being incorrectly flagged.
- LLM misinterpreting names, addresses or Hinglish responses.
- Duplicate order records distorting metrics.
- Financial assumptions overstating potential savings.
- WhatsApp delivery or replies failing.

The LLM should interpret ambiguous text and return structured outputs; deterministic rules should make the final action.

## 7. Two-Week Rollout Plan

**Week 1 — Validate and pilot**

- Audit data quality and duplicate order IDs.
- Validate rules against historical data.
- Review high-risk decisions with operations staff.
- Test WhatsApp message templates in mock mode.
- Agree on baseline metrics and financial assumptions.

**Week 2 — Controlled experiment**

- Run a small, monitored pilot with eligible orders.
- Keep a comparison group where operationally appropriate.
- Track RTO rate, delivery success, conversion, intervention cost and customer complaints.
- Review false positives and adjust thresholds.
- Expand only if measured business outcomes justify the additional friction.
