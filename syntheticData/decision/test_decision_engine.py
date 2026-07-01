import pandas as pd
from synthetic_generator import generate_user_ids, generate_cohort
from decision_engine import (
    calculate_mssd,
    apply_decision_rules,
    summarize_decisions,
    validate_prompt_counts_vary,
)


def make_test_cohort():
    user_ids = generate_user_ids(100)
    cohort_parts = []

    for i, user_id in enumerate(user_ids):
        resp_rate = 0.65 + (i % 8) * 0.04

        user_df = generate_cohort(
            users=1,
            days=7,
            ema_per_day=5,
            seed=42 + i,
            resp_rate=resp_rate,
            user_ids=[user_id],
        )

        cohort_parts.append(user_df)

    return pd.concat(cohort_parts, ignore_index=True)


def test_prompt_counts_vary_across_users():
    ema_df = make_test_cohort()

    decision_df = calculate_mssd(ema_df, window=3)

    decision_df = apply_decision_rules(
        decision_df,
        threshold_quantile=0.80,
        cooldown_minutes=60,
        max_prompts_per_day=4,
    )

    summary_df = summarize_decisions(decision_df)

    assert validate_prompt_counts_vary(summary_df)


def test_send_prompt_matches_decision_reason():
    ema_df = make_test_cohort()

    decision_df = calculate_mssd(ema_df, window=3)

    decision_df = apply_decision_rules(
        decision_df,
        threshold_quantile=0.80,
        cooldown_minutes=60,
        max_prompts_per_day=4,
    )

    assert (
        decision_df["send_prompt"]
        == (decision_df["decision_reason"] == "prompt sent")
    ).all()