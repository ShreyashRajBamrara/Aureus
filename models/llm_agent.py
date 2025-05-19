import os
from langchain.llms import OpenAI
from langchain.llms import Ollama
from dotenv import load_dotenv

load_dotenv()

# Choose model: Ollama (local) or OpenAI (cloud)
def get_llm():
    if os.getenv("OLLAMA_BASE_URL"):
        return Ollama(base_url=os.getenv("OLLAMA_BASE_URL"), model=os.getenv("OLLAMA_MODEL", "llama2"))
    else:
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

llm = get_llm()

def ask(question, history=None):
    # Simple context passing
    context = "\n".join([f"User: {u}\nAureus: {b}" for u, b in (history or [])])
    prompt = f"{context}\nUser: {question}\nAureus:"
    return llm(prompt)
