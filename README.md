# resume_builder
----------------
Repository for resume builder app

## Project Structure

resume_builder_llm_app/
├── app.py                            # Main Streamlit entrypoint
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation

├── assets/
│   └── templates/                    # Resume template files (HTML/DOCX/LaTeX)
│       ├── modern_template.docx
│       ├── minimal_template.docx
│       └── creative_template.html

├── configs/
│   └── prompts.yaml                  # System/LLM prompt templates

├── data/
│   ├── resumes/                      # Uploaded resumes
│   ├── linkedin_profiles/           # LinkedIn data (parsed or downloaded)
│   └── job_descriptions/            # Job Descriptions provided by user

├── output/
│   ├── final_resume.pdf             # Generated resume (for download)
│   └── logs/                        # Error logs, processing reports

├── src/
│   ├── __init__.py
│   ├── ui/
│   │   ├── layout.py                # Streamlit page structure and layout
│   │   └── components.py           # Custom widgets (uploaders, forms)
│   │
│   ├── parsers/
│   │   ├── resume_parser.py        # Extracts data from uploaded resumes
│   │   ├── linkedin_parser.py      # Parses LinkedIn data from URL/PDF
│   │   └── jd_parser.py            # Extracts information from job descriptions
│   │
│   ├── llm/
│   │   ├── prompt_builder.py       # Builds prompts for the LLM
│   │   ├── resume_generator.py     # LLM API interaction to generate resume
│   │   └── scoring.py              # Optional: resume vs JD relevance scoring
│   │
│   ├── template_engine/
│   │   ├── formatter.py            # Formats LLM output for templates
│   │   └── export.py               # Exports resume to PDF/DOCX
│   │
│   └── utils/
│       ├── file_handler.py         # File saving, reading, etc.
│       ├── text_cleaner.py         # Text preprocessing and cleaning
│       └── validator.py            # Validates inputs (URLs, filetypes, etc.)

└── tests/
    ├── test_parsers.py
    ├── test_prompt_builder.py
    └── test_resume_generator.py
