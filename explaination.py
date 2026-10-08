def generate_explanation(worker):

    reasons = []

    # Skill
    reasons.append("Correct skill")

    # Verification
    if worker["verified"]:
        reasons.append("Cooperative verified")

    # Availability
    if worker["available"]:
        reasons.append("Currently available")

    # Distance
    if worker["distance"] <= 1:
        reasons.append(
            f"Nearby ({worker['distance']:.2f} km)"
        )

    elif worker["distance"] <= 3:
        reasons.append(
            f"Within service area ({worker['distance']:.2f} km)"
        )

    # Quality
    if worker["rating"] >= 4.5:
        reasons.append(
            f"Good rating ({worker['rating']} ⭐)"
        )

    # Fairness
    if worker["fairness_score"] >= 0.6:
        reasons.append(
            f"Under-utilized ({worker['jobs_this_week']} jobs this week)"
        )

    return reasons