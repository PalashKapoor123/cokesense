import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# --- Define API keys at module level ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize OpenAI client (only if key exists)
openai_client = None
if OPENAI_API_KEY and OPENAI_API_KEY != "your_openai_api_key_here":
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Groq client (free AI alternative)
groq_client = None
try:
    from groq import Groq
    if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
        groq_client = Groq(api_key=GROQ_API_KEY)
except ImportError:
    pass  # Groq not installed yet

# Note: Google Imagen requires Vertex AI setup and may have costs
# Not included by default to keep everything free

# Model names
OPENAI_LLM_MODEL = "gpt-4o-mini"
GROQ_LLM_MODEL = "llama-3.3-70b-versatile"  # Fast, free model from Groq
IMAGE_MODEL = "dall-e-3"  # OpenAI DALL-E (paid, optional)

# Backward compatibility
client = openai_client  # For existing code that uses 'client'

