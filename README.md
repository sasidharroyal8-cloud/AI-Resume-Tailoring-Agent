# AI Resume Tailoring Agent

An intelligent agent that reads job postings and tailors a candidate's resume for each specific role using Groq's AI models. The system generates customized resumes optimized for each position and can email them to recruiters.

## 📋 Features

- **Intelligent Resume Tailoring**: Uses Groq's Llama 3.3 model to analyze job requirements and tailor resumes accordingly
- **Multi-Format Support**: Processes DOCX resume files and generates PDF outputs
- **Batch Processing**: Handles multiple jobs in a single run
- **Email Integration**: Automatically sends tailored resumes to recruiters (Gmail SMTP with App Password)
- **Error Handling**: Gracefully handles failures - one failed job won't stop the pipeline
- **ATS Optimization**: Incorporates job-specific keywords for Applicant Tracking Systems
- **Comprehensive Logging**: Shows detailed progress for each job

## 🗂️ Project Structure

```
AI Resume Tailoring Agent/
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create from template)
├── IMPLEMENTATION_SUMMARY.md       # Technical implementation details
├── README.md                       # This file
├── data/
│   ├── option2_job_links.xlsx     # Job metadata (title, company, URL)
│   └── option2_jobs.json          # Full job descriptions and requirements
├── resumes/
│   ├── original/
│   │   └── candidate_resume.docx  # Base resume to tailor
│   └── tailored/                  # Output: tailored resumes (auto-created)
└── src/
    ├── main.py                    # Main orchestration logic
    ├── loader.py                  # Load and merge Excel/JSON data
    ├── parser.py                  # Extract text from resume files
    ├── ai_engine.py               # Groq AI integration for tailoring
    ├── generator.py               # Save tailored resumes as PDF
    └── emailer.py                 # Send emails via Gmail
```

## ⚙️ Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Email Configuration (Gmail SMTP)
EMAIL=your_gmail@gmail.com
EMAIL_PASSWORD=your_gmail_app_password_here

# Recipient Email Configuration
RECIPIENT_EMAIL=recruiter@example.com
```

### 3. Get API Keys

- **Groq API Key**: Get from [console.groq.com/keys](https://console.groq.com/keys)
- **Gmail App Password**: 
  1. Enable 2-Step Verification on your Gmail account
  2. Generate App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
  3. Use the 16-character password (no spaces)

### 4. Run the Agent

```bash
cd src
python main.py
```

## 📋 Requirements Met

✅ **Parse job data**: Reads `option2_job_links.xlsx` and `option2_jobs.json`, joins on `id`/`#` field  
✅ **Load base resume**: Processes `candidate_resume.docx` as base resume  
✅ **AI tailoring**: Uses Groq LLM to generate tailored versions emphasizing relevant skills  
✅ **Save outputs**: Creates PDF files (e.g., `resume_alex_morgan_backend_software_engineer.pdf`)  
✅ **Email integration**: Sends one email per job with tailored resume attachment  
✅ **Error handling**: Failed jobs don't stop the pipeline from processing remaining jobs

## 📤 Sample Output

After running, you'll get tailored PDFs in `resumes/tailored/` and emails sent to recruiters with:
- Subject: "Application: [Job Title] at [Company]"
- Body: Job details and application message
- Attachment: Tailored resume PDF
cp .env.example .env
```

Edit `.env` and add:

#### OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create a new API key
- Paste it in `OPENAI_API_KEY`

#### Gmail SMTP Credentials
For sending emails, you need:
- Your Gmail address in `EMAIL`
- An **app-specific password** in `EMAIL_PASSWORD` (not your regular password)

**To get an app-specific password:**
1. Enable 2-Step Verification on your Google Account
2. Go to https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer"
4. Google will generate a 16-character password
5. Paste it in `.env` as `EMAIL_PASSWORD`

#### Recipient Email
- Set `RECIPIENT_EMAIL` to the recruiter's email (optional - defaults to placeholder)

### 3. Prepare Input Data

The project expects:
- **`data/option2_job_links.xlsx`** - Excel file with columns: `#`, `Job Title`, `Company`, `URL`, `Resume Path`
- **`data/option2_jobs.json`** - JSON file with full job details (matched by ID)
- **`resumes/original/candidate_resume.docx`** - Base resume to tailor

All three files are already provided in the project.

## 🚀 Usage

### Quick Start (Test Mode - No Emails)

```bash
python run.py --skip-email
```

This mode processes all jobs but skips sending emails. Perfect for testing!

### Full Run (With Emails)

```bash
python run.py
```

Make sure `RECIPIENT_EMAIL` is configured in `.env` before running with emails.

### What Happens

For each job, the agent:
1. ✓ Extracts text from the candidate's resume
2. ✓ Uses AI to tailor the resume for that specific role
3. ✓ Saves the tailored resume as a DOCX file in `resumes/tailored/`
4. ✓ Sends an email with the tailored resume attached (if configured)

### Output

Tailored resumes are saved as:
```
resumes/tailored/resume_Backend_Software_Engineer.docx
resumes/tailored/resume_Frontend_Engineer.docx
resumes/tailored/resume_Machine_Learning_Engineer.docx
resumes/tailored/resume_Data_Engineer.docx
resumes/tailored/resume_DevOps_Engineer.docx
```

## 📧 Email Configuration

The system sends emails with:
- **Subject**: "Application for [Job Title] at [Company]"
- **Body**: Personalized application message with job link
- **Attachment**: Tailored resume (DOCX format)

### Testing Email (Optional)
If you want to test email functionality without sending to real recruiters:
1. Set `RECIPIENT_EMAIL` to your own email in `.env`
2. Run: `python run.py`
3. Check your inbox for the test emails

## 🔧 Advanced Usage

### Process with Error Handling
The system automatically handles:
- Missing or corrupted resume files
- API rate limits or temporary outages
- Email delivery failures
- Malformed job data

One failed job won't stop the pipeline - all others will continue processing.

### Customizing Job Matching
Edit `src/loader.py` to customize how jobs are matched between Excel and JSON files. Currently matches by the `id` / `#` field.

### Customizing Resume Tailoring
Edit the prompt in `src/ai_engine.py` (the `prompt` variable) to adjust:
- AI temperature and creativity level
- Resume format and sections
- ATS keyword optimization

## 🛠️ Troubleshooting

### "OPENAI_API_KEY not found"
- ✓ Create a `.env` file
- ✓ Add your OpenAI API key
- Restart your terminal/IDE

### "Gmail authentication failed"
- ✓ Use an app-specific password (not your regular Gmail password)
- ✓ Enable 2-Step Verification on your Google Account
- ✓ Check that EMAIL matches your Gmail address

### "Resume file not found"
- ✓ Check that `resumes/original/candidate_resume.docx` exists
- ✓ Verify the path in `option2_job_links.xlsx` matches the file location

### "Error parsing PDF"
- ✓ Ensure PDFs are not encrypted
- ✓ Try converting the PDF to DOCX format

## 📊 Example Output

```
============================================================
AI RESUME TAILORING AGENT
============================================================

📂 Loading job data...
   Excel: option2_job_links.xlsx
   JSON:  option2_jobs.json

✓ Loaded 5 jobs

[1/5] Processing: Backend Software Engineer at Nexus Systems
  📄 Extracting resume text...
  ✓ Resume extracted (2845 characters)
  🤖 Tailoring resume with AI...
  ✓ Resume tailored (1523 characters)
  💾 Saving tailored resume...
  ✓ Resume saved to: resumes/tailored/resume_Backend_Software_Engineer.docx
  ⊘ Email skipped (email functionality disabled for testing)

[2/5] Processing: Frontend Engineer at Nexus Systems
  ...
```

## 🔐 Security Notes

- Never commit `.env` to version control (it's in `.gitignore`)
- Keep your OpenAI API key confidential
- Use app-specific Gmail passwords, not your main password
- Review generated resumes before sending to ensure accuracy

## 📝 License

This project is provided as-is for resume tailoring purposes.

## ❓ Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all environment variables are set correctly
3. Ensure all input files exist in the correct locations
4. Check error messages in the console output

## 🎯 Key Technologies

- **OpenAI GPT-4 Mini**: AI-powered resume tailoring
- **python-docx**: DOCX file handling
- **PyPDF2**: PDF text extraction
- **pandas**: Excel file handling
- **Gmail SMTP**: Email delivery
