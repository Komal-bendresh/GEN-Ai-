from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage , SystemMessage ,HumanMessage

model = ChatMistralAI(model="ministral-8b-2512", temperature=0.7) 

print("chosse your AI mode")
print("press 1 for Angry mode")
print("press 2 for funny mode ")
print("press 3 for sad mode")

choice = int(input("tell your response :- "))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
    mode = "You are a very funny AI agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are a very sad AI agent. You respond in a depressed and emotional tone."



messages =[
    SystemMessage(content= mode)
 ]

print("------WELCOME----- type 0 to end conversation--------")
while True :
   
    prompt = input("You : ")
    messages.append(HumanMessage(content = prompt))
    if prompt == "0" :
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content =  response.content))

    print("BOT : ",response.content)
    
    
print(messages)