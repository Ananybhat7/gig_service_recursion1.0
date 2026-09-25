import json
from distance import calculate_distance, distance_score
from quality import quality_score
from fairness import fairness_score
from scoring import final_score
from matcher import rank_workers

def save_workers(workers):
    """
    Save the updated worker data back to workers.json.
    """

    with open("workers.json", "w") as file:
        json.dump(workers, file, indent=2)

def allocate_job(job, workers):
    """
    Allocate one job to the best eligible worker.
    """

    eligible_workers = []

    # Find eligible workers
    for worker in workers:

        if not worker["verified"]:
            continue

        if not worker["available"]:
            continue

        if job["service"] not in worker["skills"]:
            continue

        # Calculate distance
        distance = calculate_distance(
            job["latitude"],
            job["longitude"],
            worker["latitude"],
            worker["longitude"]
        )

        distance_sc = distance_score(distance)

        # Calculate quality
        quality = quality_score(worker["rating"])

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
        worker_copy = worker.copy()

        worker_copy["distance"] = distance
        worker_copy["distance_score"] = distance_sc
        worker_copy["quality_score"] = quality
        worker_copy["fairness_score"] = fairness
        worker_copy["final_score"] = final

        eligible_workers.append(worker_copy)

    # No eligible worker
    if not eligible_workers:
        return None

    # Rank workers
    ranked_workers = rank_workers(eligible_workers)

    # Select best worker
    selected_worker = ranked_workers[0]

    return selected_worker

def allocate_multiple_jobs(jobs, workers):
    """
    Allocate multiple jobs sequentially.

    Each job is:
    1. Matched to the best available worker
    2. Assigned to that worker
    3. Worker workload is updated
    4. Job is completed
    5. Worker becomes available again
    """

    results = []

    for job in jobs:

        # Find best worker for this job
        worker = allocate_job(job, workers)

        if worker is None:

            results.append({
                "job_id": job["id"],
                "service": job["service"],
                "worker": None,
                "status": "No worker available"
            })

            continue

        # Find actual worker in the worker list
        for original_worker in workers:

            if original_worker["id"] == worker["id"]:

                # Increase workload
                original_worker["jobs_this_week"] += 1

                # Worker becomes busy
                original_worker["available"] = False

                break

        # Save state after assignment
        save_workers(workers)

        # Complete the job
        complete_job(worker, workers)

        results.append({
            "job_id": job["id"],
            "service": job["service"],
            "worker": worker["name"],
            "score": worker["final_score"],
            "status": "Assigned and completed"
        })

    return results

def complete_job(worker, workers):
    """
    Mark a worker's current job as completed
    and make the worker available again.
    """

    for original_worker in workers:

        if original_worker["id"] == worker["id"]:

            original_worker["available"] = True

            break

    save_workers(workers)


if __name__ == "__main__":

    # Load workers
    with open("workers.json", "r") as file:
        workers = json.load(file)

    # Load jobs
    with open("jobs.json", "r") as file:
        jobs = json.load(file)

    # Allocate all jobs
    results = allocate_multiple_jobs(
        jobs,
        workers
    )

    print("\nJob Allocation")
    print("================")

    for result in results:

        print(
            result["job_id"],
            "|",
            result["service"],
            "|",
            result["worker"],
            "|",
            result["status"]
        )