from langchain_huggingface import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv()

embedding = HuggingFaceEmbeddings(
    model_name = "BAAI/bge-small-en-v1.5"
)

texts = [
    "Hello this is Akarsh Vyas",
    "Hello your name is YouTube",
    "And you all are very beautiful"
]

vector = embedding.embed_documents(texts)

print(vector)