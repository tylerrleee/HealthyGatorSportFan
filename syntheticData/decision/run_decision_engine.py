"""
Run the decision engine without editing existing files
"""

import os
import pandas as pd
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from synthetic_generator import generate_user_ids, generate_cohort
from decision_engine import (
    calculate_mssd,
    apply_decision_rules,
    summarize_decisions,
    validate_prompt_counts_vary,
)


BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")


if __name__ == "__main__":
    USERS = 100
    DAYS = 7
    EMA_PER_DAY = 5
    SEED = 42

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    user_ids = generate_user_ids(USERS)

    # Generate each user separately so the synthetic cohort has real user-level variation.
    cohort_parts = []

    for i, user_id in enumerate(user_ids):
        resp_rate = 0.65 + (i % 8) * 0.04

        user_df = generate_cohort(
            users=1,
            days=DAYS,
            ema_per_day=EMA_PER_DAY,
            seed=SEED + i,
            resp_rate=resp_rate,
            user_ids=[user_id],
        )

        cohort_parts.append(user_df)

    ema_df = pd.concat(cohort_parts, ignore_index=True)

    decision_df = calculate_mssd(ema_df, window=3)

    decision_df = apply_decision_rules(
        decision_df,
        threshold_quantile=0.80,
        cooldown_minutes=60,
        max_prompts_per_day=4,
    )

    summary_df = summarize_decisions(decision_df)

    decision_df.to_csv(
        os.path.join(OUTPUT_DIR, "decision_log.csv"),
        index=False
    )

    summary_df.to_csv(
        os.path.join(OUTPUT_DIR, "decision_summary.csv"),
        index=False
    )

    print(decision_df[[
        "user_id",
        "timestamp",
        "ema",
        "observed_mssd",
        "user_threshold",
        "send_prompt",
        "decision_reason"
    ]].head(30))

    print(summary_df.head())

    print("Decision reason counts:")
    print(decision_df["decision_reason"].value_counts())

    print("Prompt count distribution:")
    print(summary_df["prompts_sent"].value_counts().sort_index())

    print("send_prompt matches decision_reason:")
    print((decision_df["send_prompt"] == (decision_df["decision_reason"] == "prompt sent")).all())

    validate_prompt_counts_vary(summary_df)

    print("DONE RUNNING DECISION ENGINE")