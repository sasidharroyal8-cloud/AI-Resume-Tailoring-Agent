from fpdf import FPDF
import os
import re

class ProfessionalResumePDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(20, 15, 20)

    def header(self):
        # Add a subtle header line
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.3)
        self.line(20, 12, 190, 12)

    def footer(self):
        # Add page number
        self.set_y(-10)
        self.set_font("Helvetica", 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_section_header(self, title):
        """Add a professional section header"""
        self.set_font("Helvetica", 'B', 12)
        self.set_text_color(0, 51, 102)  # Dark blue
        self.cell(0, 8, title.upper(), 0, 1, 'L')
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(self.get_x(), self.get_y(), 190, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)  # Reset to black

    def add_bullet_point(self, text, indent=5):
        """Add a bullet point with proper indentation"""
        self.set_font("Helvetica", '', 10)
        # Bullet symbol (using dash instead of bullet for compatibility)
        self.cell(indent, 5, "-", 0, 0, 'L')
        # Text with word wrapping - use remaining width
        remaining_width = self.w - self.l_margin - self.r_margin - indent
        self.multi_cell(remaining_width, 5, text, align='L')
        self.ln(1)

def parse_resume_sections(text):
    """Parse the AI-generated resume text into sections"""
    sections = {}
    current_section = None
    current_content = []

    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a section header
        upper_line = line.upper()
        if upper_line in ['NAME', 'SUMMARY', 'SKILLS', 'EXPERIENCE', 'PROJECTS', 'EDUCATION', 'CONTACT']:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = upper_line
            current_content = []
        else:
            current_content.append(line)

    # Add the last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections

def save_as_pdf(text, filename):
    """Generate a professional PDF resume"""
    # Parse sections
    sections = parse_resume_sections(text)

    # Create PDF
    pdf = ProfessionalResumePDF()
    pdf.add_page()

    # Name (Header)
    if 'NAME' in sections:
        pdf.set_font("Helvetica", 'B', 16)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 12, sections['NAME'], 0, 1, 'C')
        pdf.ln(5)

    # Contact Info (if available)
    if 'CONTACT' in sections:
        pdf.set_font("Helvetica", '', 10)
        pdf.set_text_color(0, 0, 0)
        remaining_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(remaining_width, 5, sections['CONTACT'], align='C')
        pdf.ln(5)

    # Summary
    if 'SUMMARY' in sections:
        pdf.add_section_header("Professional Summary")
        pdf.set_font("Helvetica", '', 10)
        remaining_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.multi_cell(remaining_width, 5, sections['SUMMARY'], align='L')
        pdf.ln(3)

    # Skills
    if 'SKILLS' in sections:
        pdf.add_section_header("Skills")
        skills_text = sections['SKILLS']
        # Split skills by commas or newlines
        skills = re.split(r'[,\n]', skills_text)
        for skill in skills:
            skill = skill.strip()
            if skill:
                pdf.add_bullet_point(skill)
        pdf.ln(3)

    # Experience
    if 'EXPERIENCE' in sections:
        pdf.add_section_header("Professional Experience")
        experience_text = sections['EXPERIENCE']
        # Split into job entries (assuming each job starts with a title)
        jobs = re.split(r'\n(?=[A-Z][^a-z]*\s*[-@])', experience_text)
        for job in jobs:
            job = job.strip()
            if job:
                # Format job entry
                lines = job.split('\n')
                if lines:
                    # Job title/company
                    pdf.set_font("Helvetica", 'B', 11)
                    pdf.cell(0, 6, lines[0], 0, 1, 'L')
                    # Job details
                    pdf.set_font("Helvetica", '', 10)
                    for line in lines[1:]:
                        line = line.strip()
                        if line:
                            if line.startswith('-'):
                                pdf.add_bullet_point(line[1:].strip())
                            else:
                                remaining_width = pdf.w - pdf.l_margin - pdf.r_margin
                                pdf.multi_cell(remaining_width, 5, line, align='L')
                pdf.ln(2)

    # Projects
    if 'PROJECTS' in sections:
        pdf.add_section_header("Projects")
        projects_text = sections['PROJECTS']
        # Split projects
        projects = re.split(r'\n(?=[A-Z])', projects_text)
        for project in projects:
            project = project.strip()
            if project:
                lines = project.split('\n')
                if lines:
                    # Project title
                    pdf.set_font("Helvetica", 'B', 11)
                    pdf.cell(0, 6, lines[0], 0, 1, 'L')
                    # Project details
                    pdf.set_font("Helvetica", '', 10)
                    for line in lines[1:]:
                        line = line.strip()
                        if line:
                            if line.startswith('-'):
                                pdf.add_bullet_point(line[1:].strip())
                            else:
                                remaining_width = pdf.w - pdf.l_margin - pdf.r_margin
                                pdf.multi_cell(remaining_width, 5, line, align='L')
                pdf.ln(2)

    # Education
    if 'EDUCATION' in sections:
        pdf.add_section_header("Education")
        education_text = sections['EDUCATION']
        # Split education entries
        educations = re.split(r'\n(?=[A-Z])', education_text)
        for edu in educations:
            edu = edu.strip()
            if edu:
                lines = edu.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        pdf.set_font("Helvetica", '', 10)
                        remaining_width = pdf.w - pdf.l_margin - pdf.r_margin
                        pdf.multi_cell(remaining_width, 5, line, align='L')
                pdf.ln(2)

    # Create directory and save file
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "resumes", "tailored")

    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        os.remove(output_dir)

    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, filename)
    pdf.output(path)
    return path