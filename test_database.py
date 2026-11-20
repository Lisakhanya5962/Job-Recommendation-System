
from src.database import (
    initialize_database,
    add_job,
    get_all_jobs,
    get_job_by_id
)

# Initialize database
initialize_database()

print("Database initialized successfully!")

# Add sample vacancies
job_id = add_job(
    title="Animal Production Assistant",
    company="Green Farms",
    location="Eastern Cape",
    description="Assist with daily animal production operations.",
    required_skills=[
        "Animal Production",
        "Animal Care",
        "Teamwork",
        "Communication"
    ]
)

print("\nJob added successfully!")
print("Job ID:", job_id)

# Retrieve all vacancies
jobs = get_all_jobs()

print("\n========== STORED JOBS ==========")

for job in jobs:
    print("\nID:", job["id"])
    print("Title:", job["title"])
    print("Company:", job["company"])
    print("Location:", job["location"])
    print("Required skills:", job["required_skills"])

# Retrieve one vacancy
selected_job = get_job_by_id(job_id)

print("\n========== SINGLE JOB TEST ==========")

if selected_job:
    print("Successfully retrieved:", selected_job["title"])
