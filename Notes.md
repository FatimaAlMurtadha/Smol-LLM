uv init
git init
touch .gitignore

source .venv/Scripts/activate
uv run main.py
uv add transformers
uv add "fastapi[standard]"
from transformers import pipline

uv add "fastapi[standard]" pandas pydantic python-multipart pytest
uv add torch

uv add pydantic

uv run fastapi dev app/main.py

uv sync
uv run uvicorn app.main:app --reload


uv add --dev pytest
uv run pytest tests/test_endpoints.py -v



# the flow : PromptBuilder -> LLMRunner -> ResponseParser -> main.py


# QUESTIONS:
- What is the average final score?
- Which student behaviors show the strongest positive and negative relationship with academic performance?

- empty CSV
- wrong extension
- empty question
- malformed CSV
- ask before upload



— Security


.env
CSV upload risks
prompt injection
— GDPR


personal data
no encryption
no deletion policy
— AI risks


hallucinations
small model limitations
bias
— Design choices


Runnable chain
why modularity matters
testing benefits