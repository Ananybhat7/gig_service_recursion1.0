from distance import calculate_distance, distance_score
from quality import quality_score
from fairness import fairness_score
from scoring import final_score
from explaination import generate_explanation


def rank_workers(workers):

    ranked_workers = sorted(
        workers,
        key=lambda worker: worker["final_score"],
        reverse=True
    )

    return ranked_workers


def get_recommendation(ranked_workers):

    if not ranked_workers:
        return None

    return ranked_workers[0]


def match_job(job, workers, excluded_workers=None):

    if excluded_workers is None:
        excluded_workers = []

    eligible_workers = []

    # Find eligible workers
    for worker in workers:

        # Worker must be verified
        if not worker["verified"]:
            continue

        # Worker must be available
        if not worker["available"]:
            continue

        # Worker must have required skill
        if job["service"] not in worker["skills"]:
            continue

        # Worker rejected this particular job
        if worker["id"] in excluded_workers:
            continue

        eligible_workers.append(worker)

    # No eligible workers
    if not eligible_workers:
        return None

    # Calculate scores for every eligible worker
    for worker in eligible_workers:

        # Calculate distance
        distance = calculate_distance(
            job["latitude"],
            job["longitude"],
            worker["latitude"],
            worker["longitude"]
        )

        # Convert distance to score
        distance_sc = distance_score(distance)

        # Calculate quality
        quality = quality_score(
            worker["rating"]
        )

        # Calculate fairness
        fairness = fairness_score(
            worker["jobs_this_week"]
        )

        # Calculate final score
        final = final_score(
            distance_sc,
            quality,
            fairness
        )

        # Store scores
        worker["distance"] = distance
        worker["distance_score"] = distance_sc
        worker["quality_score"] = quality
        worker["fairness_score"] = fairness
        worker["final_score"] = final
        worker["reasons"] = generate_explanation(worker)

    # Rank workers
    ranked_workers = rank_workers(eligible_workers)

    # Get best worker
    recommended_worker = get_recommendation(ranked_workers)

    # Remaining workers are alternatives
    alternatives = ranked_workers[1:]

    # Return clean result for backend
    return {
        "recommended_worker": recommended_worker,
        "score": recommended_worker["final_score"],
        "alternatives": alternatives,
        "reasons": recommended_worker["reasons"]
    }


if __name__ == "__main__":

    import json

    # Load workers
    with open("workers.json", "r") as file:
        workers = json.load(file)

    # Load job
    with open("job.json", "r") as file:
        job = json.load(file)

    # Match job
    result = match_job(job, workers)

    if result is None:

        print("No eligible workers found.")

    else:

        recommended_worker = result["recommended_worker"]

        print("\nRecommended Worker")
        print("==================")

        print(
            recommended_worker["name"],
            "| Score:",
            round(result["score"], 2)
        )

        print("\nWhy this worker?")
        print("================")

        for reason in result["reasons"]:
            print("✓", reason)

        print("\nAlternative Workers")
        print("===================")

        for worker in result["alternatives"]:

            print(
                worker["name"],
                "| Score:",
                round(worker["final_score"], 2)
            )

        # Test rejection and rematching
        excluded_workers = [recommended_worker["id"]]

        print("\nWorker Rejected:")
        print(recommended_worker["name"])

        result_after_rejection = match_job(
            job,
            workers,
            excluded_workers
        )

        if result_after_rejection is None:

            print("\nNo other workers available.")

        else:

            new_recommendation = result_after_rejection[
                "recommended_worker"
            ]

            print("\nNew Recommendation:")
            print(new_recommendation["name"])