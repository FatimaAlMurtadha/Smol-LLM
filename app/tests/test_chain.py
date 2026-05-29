from app.chain.steps import PromptBuilder, ResponseParser, LLMRunner
from app.chain.runnable import Runnable
from app.schemas import PromptInput, LLMOutput, PromptOutput
from unittest.mock import patch
from app.chain.pipeline import oracle_chain

def test_prompt_builder():

    builder = PromptBuilder(name="prompt_builder")

    data = PromptInput(
        question="What is the average score?",
        stats={"Final_Score": {"mean": 85}}
    )

    result = builder.invoke(data)
    prompt = result.prompt.lower()

    # the answer to the question is included in the prompt
    assert "what is the average score" in prompt

    # The column name is included in the prompt
    assert "final_score" in prompt

    # The dataset statistics are included in the prompt
    assert "mean" in prompt
    assert "85" in prompt

    assert "use only the provided dataset statistics" in prompt
    assert "not enough information" in prompt


def test_response_parser_basic():
    parser = ResponseParser(name="response_parser")

    output = LLMOutput(raw_text="The average is 85")
    result = parser.invoke(output)

    assert result.answer == "The average is 85"


def test_response_parser_removes_prefixes():
    parser = ResponseParser()

    output = LLMOutput(raw_text="Answer: 85")
    result = parser.invoke(output)

    assert result.answer == "85"

def test_response_parser_removes_quotes():
    parser = ResponseParser()

    output = LLMOutput(raw_text='"85"')
    result = parser.invoke(output)

    assert result.answer == "85"

# The response parser should be able to handle answers that are wrapped in multiple layers of quotes and prefixes, and still extract the clean answer.
def test_response_parser_empty_lines():
    parser = ResponseParser()

    output = LLMOutput(raw_text="\n\n  85  \n\n")
    result = parser.invoke(output)

    assert result.answer == "85"


# If the LLM output is empty or only contains whitespace, the response parser should return a default message indicating that no answer was generated.
def test_response_parser_no_content():
    parser = ResponseParser()

    output = LLMOutput(raw_text="   \n   ")
    result = parser.invoke(output)

    assert result.answer == "No answer generated."

def test_llmrunner_mocked(monkeypatch):

    def fake_generator(prompt, max_new_tokens, return_full_text, truncation):
        return [{"generated_text": "Mocked answer"}]

    runner = LLMRunner(name="llm_runner")

    monkeypatch.setattr(LLMRunner, "generator", fake_generator)

    result = runner.invoke(PromptOutput(prompt="test"))
    assert isinstance(result, LLMOutput)
    assert result.raw_text == "Mocked answer"

class Step1(Runnable[int, int]):
    def invoke(self, data: int) -> int:
        return data + 1

class Step2(Runnable[int, int]):
    def invoke(self, data: int) -> int:
        return data * 2

def test_runnable_sequence():
    chain = Step1() | Step2()
    result = chain.invoke(3)
    assert result == 8  # (3 + 1) * 2

@patch("app.chain.pipeline.LLMRunner.invoke")
def test_oracle_chain_full(mock_llm):

    mock_llm.return_value = LLMOutput(raw_text="Answer: 85")

    data = PromptInput(
        question="What is the average score?",
        stats={"Score": {"mean": 85}}
    )

    result = oracle_chain.invoke(data)

    assert result.answer == "85"