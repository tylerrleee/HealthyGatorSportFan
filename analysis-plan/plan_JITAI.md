# HealthyGatorSportsFan — JITAI Feasibility Analysis Plan

**Author:** Tien Tyler Le
**Date:** 2026-07-23
**Study:** JITAI for UF sports fans (weight loss / feeling better around Gator football events)

---

## Overview

Three data streams are collected during the study period: EMA survey responses, JITAI intervention check-ins, and Garmin wearable telemetry. For each stream, this plan specifies (1) what is computed, (2) whether analysis runs live on the dashboard or offline in R, and (3) which feasibility benchmark it addresses.

The feasibility thresholds below are informed by the synthetic sensitivity analysis (`syntheticData/decision/sensitivity_analysis.ipynb`), which simulated 150-user cohorts over 28 days across response rates of 50–95% and MSSD threshold percentiles of 70–90%.

---

## Stream 1 — EMA Survey Responses

**Source tables:** `ema`, `user`

### Computed metrics

| Metric | Formula | Unit |
|---|---|---|
| EMA Response Rate | N(status = 'responded') / N(sent_at) | proportion per participant per week |
| Response Latency | responded_at − sent_at | minutes |
| Item-level Missingness | NULL count per mood / stress / energy column | % per item |
| Mood / Stress / Energy Trajectory | 3-day rolling mean per participant | item scale |
| Within-person MSSD | mean((x_t − x_{t-1})^2) over consecutive answered EMAs | scale units² |
| AR(1) Parameter Recovery | OLS estimate of ρ̂ and σ̂ from EMA time series | dimensionless |

### Dashboard vs. offline

- **Live dashboard:** response rate %, daily EMA send/respond counts, item missingness flags per participant.
- **Offline in R:** MSSD computation, AR(1) parameter recovery (ρ̂, σ̂), regression and one-way ANOVA across compliance tiers.

### Feasibility benchmark

- **Target response rate ≥ 70%.** The sensitivity analysis shows ρ recovery error drops significantly above this floor (ANOVA p < 0.001 for |ρ̂ − ρ| across response-rate levels); σ recovery is robust across the full 50–95% range (ANOVA p = 0.50).
- **Retention rate:** proportion of enrolled participants with ≥ 1 EMA response in each study week, reported weekly.

---

## Stream 2 — JITAI Check-ins and Intervention Log

**Source tables:** `jitai_log`, `ema`, `engagement_log`

### Definition: completed check-in

A check-in is considered **complete** when all three conditions hold:

1. `jitai_log.send_prompt = TRUE` (decision engine fired the prompt), AND
2. A linked `ema` row exists with `status = 'responded'` (participant replied to the EMA), AND
3. `engagement_log` contains a matching `event_type` of `prompt_opened` or `prompt_acted` within 30 minutes of `jitai_log.triggered_at`.

Delivery alone (push sent) does not constitute completion.

### Computed metrics

| Metric | Source fields | Unit |
|---|---|---|
| Intervention Dosage | COUNT(send_prompt = TRUE) per participant | prompts per week |
| Push Delivery Funnel | push_sent_at → device_received_at → receipt_reported_at → engagement_log.occurred_at | % reaching each stage |
| Decision Audit | observed_mssd, trigger_signal, randomization_probability, randomization_draw | per-row log |
| Cooldown Compliance | min(triggered_at gap) per user per day | minutes; flag if < 60 |
| Completed Check-in Rate | N(complete) / N(send_prompt = TRUE) | proportion |

### Dashboard vs. offline

- **Live dashboard:** prompts sent per participant per week, delivery funnel rates, completed check-in rate.
- **Offline in R:** MSSD threshold calibration (are real `observed_mssd` distributions matching simulation projections at observed response rates?), dosage vs. compliance cross-tabulation.

### Feasibility benchmark

- **Target dosage: 3–7 prompts per participant per week.** At the 80th-percentile MSSD threshold and 80% response rate, the sensitivity grid projects ~4.85 prompts/week. Real dosage should be compared against this cell and flagged if it deviates by more than ±1.5 prompts/week.
- **Decision engine clarification:** the engine has two sequential stages — (1) *eligibility check*: `observed_mssd > threshold` (the MSSD signal crosses the within-person 80th percentile); (2) *randomization*: `randomization_draw < randomization_probability` determines whether the prompt is actually sent. `trigger_reason` captures the signal type; `send_prompt` reflects the randomization outcome. These must not be conflated in reporting.

---

## Stream 3 — Garmin Wearable Telemetry

**Source tables:** `heart_rate_sample`, `stress_sample`, `wearable_device`

### Computed metrics

| Metric | Definition | Unit |
|---|---|---|
| Daily Wear Time | Minutes with ≥ 1 HR sample in each 5-min epoch | hours per day |
| Wear Gap | Contiguous window with no HR sample; "not worn" if gap > 30 min | minutes |
| Stress Data Coverage at JITAI Trigger | Nearest stress_sample within ±5 min of jitai_log.triggered_at | % of triggers with coverage |
| HR at Trigger Validity | jitai_log.hr_at_trigger vs. nearest heart_rate_sample | mean absolute difference (bpm) |
| Device Sync Lag | Current time − wearable_device.last_synced_at | hours; flag if > 24 h |
| HR-MSSD | Rolling MSSD on minute-level HR, 3-observation window | bpm² |

### Dashboard vs. offline

- **Live dashboard:** wear time per participant per day, sync freshness, % of decision points with HR/stress data available.
- **Offline in R:** HR-MSSD vs. EMA-MSSD correlation (are physiological and self-report volatility signals aligned?), stress score validity against EMA stress items.

### Feasibility benchmark

- **Wear time target: ≥ 8 hours per day, ≥ 5 days per week** per participant (standard JITAI wearable threshold).
- **JITAI data coverage: ≥ 80% of decision points** should have a valid HR and stress reading within ±5 minutes of trigger. Gaps below this threshold indicate the Garmin sync cadence is insufficient for real-time decision making.

---

## Cross-stream Aggregates

| Benchmark | Computation | Target |
|---|---|---|
| Weekly Active Participants | Users with ≥ 1 EMA response AND ≥ 1 Garmin sync in the study week | Retention ≥ 80% through week 4 |
| MSSD Engine Calibration | Compare jitai_log.observed_mssd distribution to simulation projections at observed response rate | Observed dosage within ±1.5 prompts/week of grid projection |
| Non-response Clustering (MNAR check) | Test whether stress_at_trigger is elevated on EMA non-response rows vs. response rows (Mann-Whitney U) | Flag if p < 0.05 — suggests missing-not-at-random pattern |

---

## Metric Name Correction

The protocol uses the notation `Response Rate = σ_responses / σ_all_prompts`. The σ symbol is ambiguous (standard deviation vs. summation). The correct operational definition is:

> **EMA Response Rate = N_responded / N_sent** (plain count ratio, computed per participant per week)

This should be updated in the protocol document before submission.
