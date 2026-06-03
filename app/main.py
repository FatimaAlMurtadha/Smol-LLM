# FastAPI-app, endpoints
from fastapi import FastAPI, HTTPException, UploadFile, File
import logging
from app.data import load_csv, get_stats
from app.schemas import (
    AskRequest,
    PromptInput
)
from app.chain.pipeline import oracle_chain


app = FastAPI()

# Configure logging for the application. 
# The logging level is set to INFO, which means that informational messages and above (warnings, errors, critical) will be logged. 
# A logger instance is created for the current module using __name__, allowing for organized logging throughout the application.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
MODEL_NAME = "MockModel"

# Endpoint to upload a CSV file. It accepts a file upload, loads the CSV data using the load_csv function, and returns the statistics of the loaded dataset. 
# The DATA_LOADED variable is set to True after successfully loading the dataset.
@app.get("/")
def health():
    """Simple health check endpoint to verify the API is running."""
    return {"status": "OK"} 

# Endpoint to upload a CSV file. It accepts a file upload, checks if the file is a CSV, and if so, loads the data using the load_csv function. 
# The endpoint returns metadata about the loaded dataset, such as the number of rows, columns, and data types. If the uploaded file is not a CSV, it raises an HTTP 400 error.
@app.post("/data/upload")
async def upload(file: UploadFile = File(...)):
    """
    Upload a CSV file and load it into memory.
    Returns dataset metadata (rows, columns, dtypes).
    """

    logger.info(f"Upload attempt: {file.filename}")

    if not file.filename.endswith(".csv"):

        logger.warning(
            f"Rejected non-CSV file: {file.filename}"
        )
        logger.info(f"CSV loading failed: {file.filename}")
        
        raise HTTPException(400, "Only CSV allowed")

    try:

        meta = load_csv(file.file)
        logger.info(
            f"Dataset loaded successfully with {meta['rows']} rows"
        )
        return meta

    except Exception as e:
        logger.error(f"Error occurred while loading CSV: {str(e)}")

        raise HTTPException(status_code=400, detail="Failed to read CSV")
    


# Endpoint to retrieve statistics about the loaded dataset. 
# If no dataset has been uploaded (i.e., DATA_LOADED is False), it raises an HTTP 404 error indicating that no dataset is available. 
# If a dataset has been loaded, it returns the statistics of the dataset using the get_stats function.
@app.get("/data/stats")
def stats():
    """
    Return numerical statistics for the loaded dataset.
    """

    logger.info("Stats requested")
    stats = get_stats()

    if stats is None:
        logger.warning("Stats requested but no dataset uploaded")
        raise HTTPException(status_code=404, detail="No dataset uploaded")

    return stats

# Endpoint to ask a question to the AI. It accepts a POST request with a question in the request body, retrieves the dataset statistics, 
# and processes the question through the oracle_chain to generate an answer. If no dataset has been uploaded, it raises an HTTP 404 error. 
# The response includes the original question, the generated answer, and the model used for generating the answer.
@app.post("/ai/ask")
def ask_ai(body: AskRequest):
    """
    Process a user question using the dataset statistics and the oracle chain.
    """

    logger.info(f"AI question received: {body.question}")

    stats = get_stats()

    if stats is None:
        logger.warning("AI question asked but no dataset uploaded")

        raise HTTPException(
            status_code=404,
            detail="Dataset must be uploaded before asking questions"
        )
    try:

        chain_input = PromptInput(
            question=body.question,
            stats=stats
        )

        result = oracle_chain.invoke(chain_input)

        logger.info("AI response generated successfully")

        return {
            "question": body.question,
            "answer": result.answer,
            "model": MODEL_NAME
        }

    except Exception as e:

        logger.error(f"AI pipeline failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="AI processing failed"
        )   