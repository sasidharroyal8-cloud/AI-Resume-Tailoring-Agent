from loader import load_jobs
from parser import load_base_resume
from ai_engine import tailor_resume
from generator import save_as_pdf
from emailer import send_email
import os

# Get the project root directory (parent of src/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXCEL_PATH = os.path.join(PROJECT_ROOT, "data", "option2_job_links.xlsx")
JSON_PATH = os.path.join(PROJECT_ROOT, "data", "option2_jobs.json")
BASE_RESUME_PATH = os.path.join(PROJECT_ROOT, "resumes", "candidate_resume.docx")

def main():
    try:
        print("Loading data...")
        jobs = load_jobs(EXCEL_PATH, JSON_PATH)

        print("Loading base resume...")
        base_resume = load_base_resume(BASE_RESUME_PATH)

        import re

        for job in jobs:
            print(f"\nProcessing Job ID {job['id']} - {job['title']}")

            try:
                # 1. AI Tailoring
                tailored_text = tailor_resume(base_resume, job)

                if tailored_text is None:
                    print(f"Skipped job {job['id']} due to rate limit.")
                    continue

                # 2. Save PDF (sanitize filename)
                safe_title = re.sub(r"[^a-zA-Z0-9_\- ]", "_", job['title'])
                safe_title = re.sub(r"_+", "_", safe_title.replace(' ', '_')).strip('_').lower()
                filename = f"resume_alex_morgan_{safe_title}.pdf"
                pdf_path = save_as_pdf(tailored_text, filename)

                print(f"Resume saved: {pdf_path}")

                # 3. Send Email
                send_email(job, pdf_path)

            except Exception as e:
                print(f"Failed job {job['id']}: {e}")
                continue  # IMPORTANT: continue pipeline

        print("\nAll jobs processed!")
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()