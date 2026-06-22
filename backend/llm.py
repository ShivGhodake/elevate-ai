import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("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"),
    model_name=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
)

def run_llm(prompt):
    response = llm.invoke(prompt)
    return response.content
