import os
import time
import socket
from groq import Groq, RateLimitError
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

# Create client with timeout
client = Groq(api_key=api_key, timeout=120.0)


def tailor_resume(base_resume, job, attempts=3, backoff=10):
    prompt = f"""
You are a professional resume tailoring assistant. Create a tailored resume that highlights relevant experience and skills for this specific job.

BASE RESUME:
{base_resume}

JOB DETAILS:
Title: {job['title']}
Company: {job['company']}
Description: {job['description']}
Requirements: {job['requirements']}
Nice to Have: {job['nice_to_have']}

INSTRUCTIONS:
- Tailor the resume specifically for this role
- Emphasize relevant skills and experience
- Use ATS-friendly keywords from the job description
- Keep content concise and professional
- Focus on achievements and quantifiable results

OUTPUT FORMAT - Use these exact section headers:

NAME
[Full Name]

SUMMARY
[2-3 sentence professional summary tailored to the job]

SKILLS
[Comma-separated list of relevant technical and soft skills]

EXPERIENCE
[Job Title/Company - Dates]
- [Achievement/responsibility 1]
- [Achievement/responsibility 2]
- [Achievement/responsibility 3]

[Next Job Title/Company - Dates]
- [Achievement/responsibility 1]
- [Achievement/responsibility 2]

PROJECTS
[Project Name/Title]
- [Project description and technologies used]
- [Key achievements or results]

[Next Project Name/Title]
- [Project description and technologies used]

EDUCATION
[Degree/Program - Institution - Year]
[Relevant coursework or achievements]

[Previous Degree - Institution - Year]
"""

    for attempt in range(1, attempts + 1):
        try:
            print(f"  AI Tailoring (attempt {attempt}/{attempts})...")
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4
            )

            return response.choices[0].message.content

        except RateLimitError as rl_err:
            # If we are at token limit, immediate skip to avoid waiting and block.
            print(f"[WARNING] Rate limit hit for {job['title']} ({job['company']}): {rl_err}")
            return None

        except (socket.timeout, TimeoutError) as timeout_err:
            if attempt < attempts:
                print(f"[WARNING] Timeout on attempt {attempt}, waiting {backoff}s before retry...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                print(f"[ERROR] Timeout after {attempts} attempts for {job['title']}")
                return None

        except Exception as e:
            if attempt < attempts:
                print(f"[WARNING] AI Error on attempt {attempt}: {e}, retrying...")
                time.sleep(backoff)
            else:
                print(f"[ERROR] AI Error after {attempts} attempts: {e}")
                raise
    
    return None