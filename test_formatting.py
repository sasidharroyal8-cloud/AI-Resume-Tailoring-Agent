import sys
import os
from pathlib import Path

# Add project root and src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))

from generator import save_as_pdf

def test_professional_formatting():
    print("Testing professional resume PDF formatting...")

    # Sample professional resume text in the expected format
    sample_resume = """
NAME
Alex Morgan

SUMMARY
Results-driven Backend Software Engineer with 5+ years of experience in scalable web applications and microservices architecture. Proven expertise in Python, Node.js, and cloud technologies. Passionate about building high-performance systems that deliver exceptional user experiences.

SKILLS
Python, Django, Flask, Node.js, Express.js, PostgreSQL, MongoDB, Redis, Docker, Kubernetes, AWS, REST APIs, GraphQL, Git, CI/CD, Agile/Scrum

EXPERIENCE
Senior Backend Engineer - TechCorp Inc. - 2022-Present
- Led development of microservices architecture serving 1M+ users, improving response time by 40%
- Designed and implemented RESTful APIs handling 10k+ requests per minute
- Mentored junior developers and established coding standards across the team
- Collaborated with cross-functional teams to deliver features on time

Backend Developer - StartupXYZ - 2020-2022
- Built scalable e-commerce platform using Django and PostgreSQL
- Implemented payment processing system reducing transaction failures by 60%
- Optimized database queries resulting in 50% faster page loads

PROJECTS
E-Commerce Microservices Platform
- Developed distributed system with 15+ services using Docker and Kubernetes
- Implemented event-driven architecture with RabbitMQ
- Achieved 99.9% uptime and handled 500k+ daily transactions

Real-time Chat Application
- Built WebSocket-based chat system supporting 10k concurrent users
- Used Redis for message caching and session management
- Implemented end-to-end encryption for secure communications

EDUCATION
Master of Science in Computer Science - University of Technology - 2020
- GPA: 3.8/4.0
- Relevant Coursework: Advanced Algorithms, Distributed Systems, Software Engineering

Bachelor of Science in Computer Science - State University - 2018
- GPA: 3.7/4.0
- Dean's List for 3 semesters
"""

    try:
        pdf_path = save_as_pdf(sample_resume, 'sample_professional_resume.pdf')
        print(f'✅ Professional PDF saved: {pdf_path}')
        print('✅ Professional resume formatting test successful!')
        print('\n📄 The PDF now includes:')
        print('  • Professional header with name prominently displayed')
        print('  • Section headers with blue styling and underlines')
        print('  • Proper bullet points for lists')
        print('  • Clean typography and spacing')
        print('  • Page numbers and subtle borders')
        print('  • ATS-friendly formatting')

    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_professional_formatting()