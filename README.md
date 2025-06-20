# resume_builder
----------------
Repository for resume builder app

## Project Structure

resume_builder_llm_app/
├── app.py # Streamlit app entrypoint
├── requirements.txt # Python dependencies
├── README.md # Project documentation

├── assets/
│ └── templates/ # Resume templates (HTML/DOCX/LaTeX)

├── configs/
│ └── prompts.yaml # LLM system & user prompt templates

├── data/
│ ├── resumes/ # Uploaded resume files
│ ├── linkedin_profiles/ # Parsed LinkedIn data
│ └── job_descriptions/ # Uploaded JD files or text

├── output/
│ ├── final_resume.pdf # Final resume output
│ └── logs/ # Logs or error reports

├── src/
│ ├── ui/ # Streamlit UI layout & components
│ │ ├── layout.py
│ │ └── components.py
│ │
│ ├── parsers/ # Resume, LinkedIn, and JD parsers
│ │ ├── resume_parser.py
│ │ ├── linkedin_parser.py
│ │ └── jd_parser.py
│ │
│ ├── llm/ # LLM interaction logic
│ │ ├── prompt_builder.py
│ │ ├── resume_generator.py
│ │ └── scoring.py
│ │
│ ├── template_engine/ # Resume formatting and exporting
│ │ ├── formatter.py
│ │ └── export.py
│ │
│ └── utils/ # Helper utilities
│ ├── file_handler.py
│ ├── text_cleaner.py
│ └── validator.py

└── tests/ # Unit and integration tests
├── test_parsers.py
├── test_prompt_builder.py
└── test_resume_generator.py
