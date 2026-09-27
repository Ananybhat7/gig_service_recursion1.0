from distance import distance_score
from quality import quality_score
from fairness import fairness_score
from scoring import final_score


# Test 1: Distance score
print("TEST 1: Distance Score")
print("_______________________")

near = distance_score(1)
far = distance_score(4)

print("1 km score:", near)
print("4 km score:", far)

assert near > far

print("PASS ✅")

# Test 2: Fairness score
print("\nTEST 2: Fairness Score")
print("_________________________")

under_utilized = fairness_score(1)
highly_utilized = fairness_score(8)

print("Worker with 1 job:", under_utilized)
print("Worker with 8 jobs:", highly_utilized)

assert under_utilized > highly_utilized

print("PASS ✅")

# Test 3: Full Matching Score
print("\nTEST 3: Full Matching Score")
print("______________________________")

# Rajesh
rajesh_distance = distance_score(0.63)
rajesh_quality = quality_score(4.9)
rajesh_fairness = fairness_score(8)

rajesh_final = final_score(
    rajesh_distance,
    rajesh_quality,
    rajesh_fairness
)


# Suresh
suresh_distance = distance_score(0.44)
suresh_quality = quality_score(4.6)
suresh_fairness = fairness_score(1)

suresh_final = final_score(
    suresh_distance,
    suresh_quality,
    suresh_fairness
)


print("Rajesh final score:", round(rajesh_final, 2))
print("Suresh final score:", round(suresh_final, 2))


# Suresh should rank higher in this scenario
assert suresh_final > rajesh_final

print("PASS ✅")

# Test 4: Fairness should not overpower quality
print("\nTEST 4: Fairness vs Quality")
print("---------------------------")

# Worker A: excellent worker, nearby, already received some jobs
worker_a_distance = distance_score(0.5)
worker_a_quality = quality_score(5.0)
worker_a_fairness = fairness_score(4)

worker_a_final = final_score(
    worker_a_distance,
    worker_a_quality,
    worker_a_fairness
)


# Worker B: under-utilized, but far away and lower rated
worker_b_distance = distance_score(4.5)
worker_b_quality = quality_score(3.0)
worker_b_fairness = fairness_score(0)

worker_b_final = final_score(
    worker_b_distance,
    worker_b_quality,
    worker_b_fairness
)


print("Worker A final score:", round(worker_a_final, 2))
print("Worker B final score:", round(worker_b_final, 2))


# Worker A should win
assert worker_a_final > worker_b_final

print("PASS ✅")