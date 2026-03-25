import os
from abc import ABC
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class BaseAgent(ABC):
    def __init__(self, model_env_key: str = "GROQ_MODEL", default_model: str = "llama-3.1-8b-instant"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv(model_env_key, default_model)
        self.fallback_models = [
            self.model,
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ]
