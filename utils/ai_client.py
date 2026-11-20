import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_client():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "")

    if not endpoint or not api_key:
        raise EnvironmentError("Azure credentials missing. Check your .env file.")

    return OpenAI(
        base_url=endpoint.rstrip("/") + "/",
        api_key=api_key
    )

def chat(messages: list, temperature: float = 0.7) -> str:
    client = get_client()
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")

    response = client.chat.completions.create(
        model=deployment,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content
