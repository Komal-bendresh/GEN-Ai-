from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model("openai/gpt-oss-120b", model_provider="groq", temperature = 0.8, max_tokens =200 )

response = model.invoke("write a poem on human")

print(response.content)

