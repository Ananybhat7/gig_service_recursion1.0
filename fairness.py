def fairness_score(jobs_this_week, target_jobs=5):
    score = 1 - min(jobs_this_week / target_jobs, 1)
    return score