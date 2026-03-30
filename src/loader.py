import pandas as pd
import json

def load_jobs(excel_path, json_path):
    df = pd.read_excel(excel_path)

    with open(json_path, "r") as f:
        jobs_json = json.load(f)["jobs"]

    # Convert JSON list → dict by id
    jobs_dict = {job["id"]: job for job in jobs_json}

    merged_jobs = []

    for _, row in df.iterrows():
        job_id = int(row["#"])

        if job_id not in jobs_dict:
            continue

        job_json = jobs_dict[job_id]

        merged_jobs.append({
            "id": job_id,
            "title": job_json["title"],
            "company": job_json["company"],
            "url": job_json["url"],
            "description": job_json["description"],
            "requirements": job_json["requirements"],
            "nice_to_have": job_json.get("nice_to_have", [])
        })

    return merged_jobs