# Översikt

Detta projekt är en komplett AI‑driven datanalystjänst byggd med FastAPI, Pandas, Pydantic, och en lokal språkmodell (SmolLM2‑135M‑Instruct).  
Användaren laddar upp en CSV‑fil, tjänsten beräknar statistik, och användaren kan sedan ställa frågor om datan via ett AI‑gränssnitt.

Systemet använder en Runnable‑kedja:

`
PromptBuilder -> LLMRunner -> ResponseParser
`

Denna kedja bygger prompten, kör modellen och extraherar ett kort och tydligt svar.

---

# Installation

1. Klona projektet

`bash
git clone https://github.com/FatimaAlMurtadha/Smol-LLM.git
cd Smol-LLM
`

2. Synka och installera alla beroenden via uv
   uv sync

3. Starta servern

`bash
 uv run uvicorn app.main:app --reload
`
OBS: Använd INTE venv. Projektet använder uv:s egna miljö (.uv/).
Om du har en .venv-mapp, ta bort den innan du kör:

rm -rf .venv
uv sync
uv run uvicorn app.main:app --reload

Servern körs nu på: ` http://127.0.0.1:8000 `

---

# Swagger / API‑dokumentation

Swagger finns automatiskt på:

`
http://127.0.0.1:8000/docs
`

---

### 1. Ladda upp dataset

Swagger
Gå till /data/upload -> välj en .csv -> kör.

OBS: Du kan ladda up et exampel på dataset här: https://www.kaggle.com/datasets/sarveshchhetri/student-lifestyle-vs-academic-performance-dataset/data [ELLER använda det datasetet i rooten](/student_performance_finalscore.csv)

curl‑exempel

`bash
curl -X POST -F "file=@data.csv" http://127.0.0.1:8000/data/upload
`

Exempelsvar:

`json
{
  "rows": 8000,
  "columns": [
    "Student_ID",
    "Age",
    "Gender",
    "Hours_Studied",
    "Attendance",
    "Sleep_Hours",
    "Stress_Level",
    "Screen_Time",
    "Previous_GPA",
    "Part_Time_Job",
    "Study_Method",
    "Diet_Quality",
    "Internet_Quality",
    "Extracurricular",
    "Tutoring_Sessions_Per_Week",
    "Family_Income_Level",
    "Exam_Anxiety_Score",
    "Final_Score"
  ],
  "dtypes": {
    "Student_ID": "str",
    "Age": "int64",
    "Gender": "str",
    "Hours_Studied": "float64",
    "Attendance": "float64",
    "Sleep_Hours": "float64",
    "Stress_Level": "float64",
    "Screen_Time": "float64",
    "Previous_GPA": "float64",
    "Part_Time_Job": "str",
    "Study_Method": "str",
    "Diet_Quality": "str",
    "Internet_Quality": "str",
    "Extracurricular": "str",
    "Tutoring_Sessions_Per_Week": "int64",
    "Family_Income_Level": "str",
    "Exam_Anxiety_Score": "float64",
    "Final_Score": "float64"
  }
}
`

---

### 2. Hämta statistik

`bash
curl http://127.0.0.1:8000/data/stats
`

Exempelsvar:

`json
{
  "Age": {
    "count": 8000,
    "mean": 20.494375,
    "std": 2.2859618461536617,
    "min": 17,
    "25%": 18,
    "50%": 20.5,
    "75%": 22,
    "max": 24
  },
  "Hours_Studied": {
    "count": 8000,
    "mean": 4.9838450000000005,
    "std": 1.9517146793905913,
    "min": 0.02,
    "25%": 3.68,
    "50%": 4.98,
    "75%": 6.3125,
    "max": 12
  },
  "Attendance": {
    "count": 8000,
    "mean": 79.933375,
    "std": 9.65659359372415,
    "min": 43.3,
    "25%": 73.4,
    "50%": 80.1,
    "75%": 86.6,
    "max": 100
  },
  "Sleep_Hours": {
    "count": 8000,
    "mean": 6.989125,
    "std": 1.1928975689267054,
    "min": 3,
    "25%": 6.2,
    "50%": 7,
    "75%": 7.8,
    "max": 10
  },
  "Stress_Level": {
    "count": 8000,
    "mean": 5.014174999999999,
    "std": 1.940125532088074,
    "min": 1,
    "25%": 3.7,
    "50%": 5,
    "75%": 6.3,
    "max": 10
  },
  "Screen_Time": {
    "count": 8000,
    "mean": 4.024525,
    "std": 1.4819077335284192,
    "min": 0.5,
    "25%": 3,
    "50%": 4,
    "75%": 5,
    "max": 9.6
  },
  "Previous_GPA": {
    "count": 8000,
    "mean": 2.9924075,
    "std": 0.48952998773809747,
    "min": 1.5,
    "25%": 2.67,
    "50%": 2.99,
    "75%": 3.33,
    "max": 6.7
  },
  "Tutoring_Sessions_Per_Week": {
    "count": 8000,
    "mean": 1.700625,
    "std": 1.1128362008517878,
    "min": 0,
    "25%": 1,
    "50%": 2,
    "75%": 2,
    "max": 5
  },
  "Exam_Anxiety_Score": {
    "count": 8000,
    "mean": 4.4942375000000006,
    "std": 1.6855713237444683,
    "min": 1,
    "25%": 3.3,
    "50%": 4.4,
    "75%": 5.6,
    "max": 10
  },
  "Final_Score": {
    "count": 8000,
    "mean": 83.20564875,
    "std": 12.756728127470156,
    "min": 22.81,
    "25%": 75.50750000000001,
    "50%": 86.51,
    "75%": 93.08,
    "max": 99.98
  }
}
`

---

### 3. Ställ en AI‑fråga

`bash
curl -X POST http://127.0.0.1:8000/ai/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the average score?"}'
`

Exempelsvar:

`json
{
  "question": "What is the average score?",
  "answer": "The average score is 84.43%.",
  "model": "MockModel"
}
`

> Notera:  
> I verklig körning används den riktiga modellen.  
> I tester mockas modellen för att göra resultaten deterministiska.

---

## Hur kedjan fungerar

PromptBuilder
- Tar emot användarens fråga + statistik  
- Bygger en strikt prompt  
- Tvingar modellen att endast använda statistiken  

LLMRunner
- Kör SmolLM2‑modellen lokalt  
- Lazy‑loading för snabbare start  
- Mockas i tester  

ResponseParser
- Extraherar första meningsfulla raden  
- Tar bort prefix som “Answer:”  
- Returnerar ett rent svar  

---

## Projektstruktur

`
app/
 ├── main.py               # API-endpoints
 ├── data.py               # CSV-hantering och statistik
 ├── schemas.py            # Pydantic-modeller
 ├── chain/
 │    ├── runnable.py      # Runnable-bas och kedjelogik
 │    ├── steps.py         # PromptBuilder, LLMRunner, ResponseParser
 │    └── pipeline.py  
 ├── tests/
 │    ├── test_chain.py
 │    ├── test_endpoints.py    # oracle_chain
 └── ...
`

---

## Antaganden

- Användaren laddar alltid upp datasetet själv via /data/upload.  
- Datasetet lagras endast i RAM och sparas aldrig på disk.  
- Endast numeriska kolumner används i statistiken (pandas.DataFrame.describe()).  
- Modellen ska endast använda statistik — inte hela datasetet.  
- I tester mockas modellen för att undvika långsamma och icke‑deterministiska svar.  
- Tjänsten är en prototyp och inte avsedd för personuppgifter (GDPR‑skäl).

---

### Köra tester
#### 1. Endpoints

`bash
uv run pytest app/tests/test_endpoints.py -v
`

#### 2. Chain

`bash
uv run pytest app/tests/test_chain.py -v
`

Tester inkluderar:

- Runnable‑steg  
- hela kedjan  
- API‑endpoints  
- mockad LLMRunner  

---

## Slutsats

Detta projekt demonstrerar:

- modulär AI‑arkitektur  
- robust testning  
- säker filhantering  
- tydlig separation av ansvar  
- en fungerande kedja från data -> statistik -> AI‑svar  

Systemet är lätt att utöka och anpassa för framtida behov.