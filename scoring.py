def final_score(distance_score_value, quality_score_value, fairness_score_value):
    score = (
        0.40 * distance_score_value
        + 0.40 * quality_score_value
        + 0.20 * fairness_score_value
    )
    return score