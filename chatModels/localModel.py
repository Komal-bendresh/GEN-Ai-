from dotenv import load_dotenv
from langchain_community.llms import Ollama

load_dotenv()

# Initialize local Ollama model
llm = Ollama(model="mistral", temperature=0.8)

response = llm.invoke("What is a local language model?")

print(response)
  