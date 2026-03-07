 # Classifies prompt complexity
 
from models import call_simple_model

CLASSIFIER_PROMPT = """You are a prompt complexity classifier.
Classify the following user prompt as either 'simple' or 'complex'.

Simple = greetings, small talk, basic facts, short one-line questions
Complex = analysis, coding, reasoning, architecture, multi-step problems

Respond with ONLY one word: simple or complex

Prompt: {prompt}"""

def classify_complexity(message: str) -> str:
    result = call_simple_model(
        CLASSIFIER_PROMPT.format(prompt=message)
    )
    result = result.strip().lower()
    return "complex" if "complex" in result else "simple"