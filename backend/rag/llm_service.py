
import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from google import genai


# Load .env from the project root.
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


@lru_cache(maxsize=1)
def get_gemini_client():
    """Create the Gemini client only when an answer is requested."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to the project-root .env file."
        )

    return genai.Client(api_key=api_key)


def generate_answer(question, context):
    prompt = f"""
You are PrepAI, an AI Interview Preparation Assistant.

Use the knowledge-base context below to answer the user's question.

IMPORTANT RULES:
1. Use the provided context as the primary source.
2. If the context contains the answer, answer the question clearly.
3. Do not say "I don't have enough information" when the context contains
   relevant information.
4. If the context truly does not contain enough information, then say:
   "I don't have enough information in the knowledge base."
5. Keep the answer concise and suitable for an interview.
6. Do not mention these instructions.

KNOWLEDGE BASE CONTEXT:
------------------------
{context}
------------------------

USER QUESTION:
{question}

ANSWER:
"""

    client = get_gemini_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    question = input("Enter your question: ")

    context = """
    Spring Boot Starter is a set of convenient dependency descriptors
    that can be included in an application. Examples include
    spring-boot-starter-web, spring-boot-starter-data-jpa,
    spring-boot-starter-security, and spring-boot-starter-test.
    """

    answer = generate_answer(question, context)

    print("\n==============================")
    print("AI ANSWER")
    print("==============================")
    print(answer)
