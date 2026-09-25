import json


# Original demo worker data
original_workers = [
    {
        "id": "W001",
        "name": "Rajesh Kumar",
        "skills": ["plumbing"],
        "verified": True,
        "available": True,
        "rating": 4.9,
        "jobs_this_week": 8,
        "latitude": 12.9750,
        "longitude": 77.5900
    },
    {
        "id": "W002",
        "name": "Suresh Kumar",
        "skills": ["plumbing"],
        "verified": True,
        "available": True,
        "rating": 4.6,
        "jobs_this_week": 1,
        "latitude": 12.9755,
        "longitude": 77.5950
    },
    {
        "id": "W003",
        "name": "Imran Khan",
        "skills": ["plumbing"],
        "verified": True,
        "available": True,
        "rating": 4.7,
        "jobs_this_week": 4,
        "latitude": 12.9800,
        "longitude": 77.6000
    },
    {
        "id": "W004",
        "name": "Anita Sharma",
        "skills": ["electrical"],
        "verified": True,
        "available": True,
        "rating": 4.9,
        "jobs_this_week": 2,
        "latitude": 12.9700,
        "longitude": 77.5920
    },
    {
        "id": "W005",
        "name": "Ravi Kumar",
        "skills": ["plumbing"],
        "verified": True,
        "available": False,
        "rating": 5.0,
        "jobs_this_week": 3,
        "latitude": 12.9720,
        "longitude": 77.5930
    }
]


# Write original data back to workers.json
with open("workers.json", "w") as file:
    json.dump(original_workers, file, indent=2)


print("Worker data has been reset successfully! ✅")