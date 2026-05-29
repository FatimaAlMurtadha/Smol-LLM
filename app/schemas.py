from pydantic import BaseModel, Field
from typing import Dict, Any


# This schema defines the structure of the request body for an API endpoint that accepts a question. The AskRequest model has a single field, 'question', which is a string. This model can be used to validate incoming requests to ensure they contain the expected data format.
class AskRequest(BaseModel):
    """
    Schema for the /ai/ask endpoint.
    Ensures the question is a non‑empty string.
    """
    question: str = Field(min_length=1) # must be a non-empty string / the question cannot be an empty string

# These schemas define the structure of the data used in the application. PromptInput represents the input for generating a prompt, containing a question and associated statistics. PromptOutput represents the output of the prompt generation process, containing the generated prompt as a string. LLMOutput represents the raw text output from a language model, while ParsedAnswer represents a structured answer extracted from the raw text, containing just the answer as a string. These models can be used for data validation and serialization in API endpoints or other parts of the application that handle these types of data.
class PromptInput(BaseModel):
    """
    Input to the PromptBuilder step.
    Contains the user question and dataset statistics.
    """
    question: str = Field(min_length=1)
    stats: dict  # column -> {stat_name: value}

# The PromptOutput model represents the output of a prompt generation process, containing the generated prompt as a string. This model can be used to structure the response from an API endpoint that generates prompts based on input data.
class PromptOutput(BaseModel):
    """
    Output of PromptBuilder.
    Contains the fully constructed prompt string.
    """
    prompt: str

# The LLMOutput model represents the raw text output from a language model, while the ParsedAnswer model represents a structured answer extracted from the raw text. The LLMOutput contains a single field, 'raw_text', which is a string representing the unprocessed output from the language model. The ParsedAnswer contains a single field, 'answer', which is a string representing the extracted answer from the raw text. These models can be used for data validation and serialization in API endpoints or other parts of the application that handle interactions with language models.
class LLMOutput(BaseModel):
    """
    Raw output from the language model.
    """
    raw_text: str

# The ParsedAnswer model represents a structured answer extracted from the raw text output of a language model. It contains a single field, 'answer', which is a string representing the extracted answer. This model can be used to structure the response from an API endpoint that processes the raw output from a language model and extracts a specific answer for the client.
class ParsedAnswer(BaseModel):
    """
    Final cleaned answer extracted from the LLM output.
    """
    answer: str = Field(min_length=1)