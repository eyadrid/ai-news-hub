import os
from typing import Optional
import json
from groq import Groq
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class DigestOutput(BaseModel):
    title: str
    summary: str

PROMPT = """You are an expert AI news analyst specializing in summarizing technical articles, research papers, and video content about artificial intelligence.

Your role is to create concise, informative digests that help readers quickly understand the key points and significance of AI-related content.

Guidelines:
- Create a compelling title (5-10 words) that captures the essence of the content
- Write a 2-3 sentence summary that highlights the main points and why they matter
- Focus on actionable insights and implications
- Use clear, accessible language while maintaining technical accuracy
- Avoid marketing fluff - focus on substance

Always respond with valid JSON in this format:
{"title": "...", "summary": "..."}"""


class DigestAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.fallback_models = [
            self.model,
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
        ]
        self.system_prompt = PROMPT

    def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
        try:
            user_prompt = f"Create a digest for this {article_type}: \n Title: {title} \n Content: {content[:8000]}"

            last_error = None
            for model_name in dict.fromkeys(self.fallback_models):
                try:
                    response = self.client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.7,
                        response_format={"type": "json_object"}
                    )

                    response_text = response.choices[0].message.content
                    response_json = json.loads(response_text)

                    return DigestOutput(
                        title=response_json.get("title", ""),
                        summary=response_json.get("summary", "")
                    )
                except Exception as e:
                    last_error = e

            if last_error:
                raise last_error

            return None
        except Exception as e:
            print(f"Error generating digest: {e}")
            return None
