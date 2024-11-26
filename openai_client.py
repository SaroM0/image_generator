import openai
import os

def initialize_openai():
    openai.api_key = os.getenv("OPENAI_API_KEY")
