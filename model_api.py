import os
from dotenv import load_dotenv
import sys

from llama_index.llms.gemini import Gemini
from IPython.display import Markdown, display
from transformers import pipeline
from exception import customexception
from logger import logging

load_dotenv()

def load_model():
    """
    Loads a text generation model for natural language processing using Hugging Face transformers library.

    Returns:
    - pipeline: An instance of the Hugging Face text generation pipeline.
    """
    try:
        model = pipeline("text-generation", model="gpt2")
        return model
    except Exception as e:
        raise customexception(e, sys)

# Example usage
if _name_ == "_main_":
    model = load_model()
    input_text = "Once upon a time"
    response = model(input_text, max_length=50, num_return_sequences=1)
    print(response)
