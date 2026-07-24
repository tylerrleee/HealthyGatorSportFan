Tien: the analysis plan, one to two pages. For each of the three data streams, survey, check-ins, watch, what exactly we compute, 
live on the dashboard or offline in R, mapped to the feasibility benchmarks in the protocol. 
Plus your two document fixes, the metric name and the engine description, both submission ready by Friday.


# Data Streams

## Survey responses (EMA)
    - Reponse rate per participant per week : 
        ``` COUNT(status = 'responded') / COUNT(sent_at) from ema ```
        - Goal: sensitivity analysis shows >=80% is the floor for reliable \rho recovery
    - Time to respond: 
        ``` responded_at - sent_at from ema ```
        ` Goal compliance quality metric
    - Temporal trends of mood/stress/energy
        - Rolling 3-day mean per participant
    - Within-person MSSD

## Check-ins (prompt-intervention)
    - Completed definition: delivery AND engagement AND response
        - A jitai_log row where send_prompt = True AND an ema row with status = 'responded' AND engagement_log shows event_type = 'completed' 
    - Intervention count: 
        - COUNT(send_prompt = True) per participant per week, group by trigger_signal and threshold_quantile
    - Decision audit: 
        - for each jitai_log row, get observed_mssd, randomization_probability, randomization_draw, trigger_reason
        - Goal: explain why prompt was sent (trigger metadata)
    - Push delivery latency or observablity:
        - Get gap between push_sent_at -> device_received_at -> receipt_reported_at -> engagement_log.occured_at
        - Goal: Does how fast a prompt trigger gets sent a participant affect their EMA response after?
    - Cooldown Complianace / Prompt fatigue:
        - verify that current triggered_at and LAG(triggered_at) timestamps per participant are >= 60 min (change by decision engine constraint).

## Garmin telemetry
    - Wear time per day: 
        - COUNT(EXTRACT minute FROM bpm) from heart_rate_sample. 
        - Get wear cap = contigous window with no HR sample
        - "Worn" means >= 1 bpm sample in a 5-min epoch, "not worn" means > 30min gap
    - Stress sample coverage: 
        - Join jitai_log and stress_sample within a 5 minute window
        - Goal: are stress scores available at JITAI decision?
        - If JITAI prompt triggered but has no stress score, it is a data coverage issue -- consider for a false positive.
    - HR at JITAI trigger
        - comparing to jitai_log.hr_at_trigger
        - Validate against heart_rate_sample to confirm decision engine was reading the same data
        - Assess whether JITAI trigger caused an incremental change to HR and MSSD
    - MSSD / HR Volatility:
        - rolling MSSD on minute-level
        - HR from heart_rate_sample.bpm

Feasibility benchmark mapping:
- Response rate benchmark directly: n_responded / n_sent per week, flagging participants below 70%.
- Retention rate: count of users with ≥1 EMA response in each study week.
- "Completed check-in" operationalization: define it once, compute it from jitai_log + engagement_log join.
- Dosage benchmark: compare observed prompts/week to the sensitivity grid's projected values — a 80th pct threshold at actual response rate should match the notebook's cells.
- Wear time benchmark: % of days with ≥8 hours worn per participant (common JITAI threshold).
- Wear gap benchmark: mean gap duration and % of JITAI decision points where HR data was unavailable.

Cross-stream / Aggregate

- Participant retention rate: weekly active users (>=1 EMA response + >=1 Garmin sync) over study weeks.
- MSSD calibration check: compare jitai_log.observed_mssd distributions to what the sensitivity analysis predicted at the observed response rate -- validates whether the live engine is behaving like the simulation.
- Non-response clustering: are EMA non-responses clustered (MNAR - e.g., missing when stressed)? Test using stress_at_trigger on non-response rows.
