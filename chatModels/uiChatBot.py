# import streamlit as st
# from dotenv import load_dotenv

# load_dotenv()

# from langchain_mistralai import ChatMistralAI
# from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# st.title("SAD AI Chatbot")

# model = ChatMistralAI(model="ministral-8b-2512", temperature=0.7)

# # Keep conversation history across Streamlit reruns
# if "messages" not in st.session_state:
#     st.session_state.messages = [SystemMessage(content="you are a SAD AI agent and reply every message in sad way")]

# # Show previous messages (skip the system message)
# for msg in st.session_state.messages:
#     if isinstance(msg, HumanMessage):
#         with st.chat_message("user"):
#             st.write(msg.content)
#     elif isinstance(msg, AIMessage):
#         with st.chat_message("assistant"):
#             st.write(msg.content)

# # Chat input
# prompt = st.chat_input("You :")

# if prompt:
#     st.session_state.messages.append(HumanMessage(content=prompt))
#     with st.chat_message("user"):
#         st.write(prompt)

#     response = model.invoke(st.session_state.messages)
#     st.session_state.messages.append(AIMessage(content=response.content))

#     with st.chat_message("assistant"):
#          st.write(response.content)


import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ---------- Page setup ----------
st.set_page_config(page_title="Chatty", page_icon="🤖", layout="centered")

st.markdown(
    """
    <style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {padding-top: 2rem; max-width: 780px;}

    .hero {
        text-align: center;
        padding: 1.4rem 1rem;
        margin-bottom: 1.2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
    }
    .hero h1 {margin: 0; font-size: 2rem; color: white;}
    .hero p {margin: 0.3rem 0 0; opacity: 0.9;}

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        background: rgba(120, 120, 160, 0.10);
    }
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(120, 120, 160, 0.35);
        padding: 0.6rem;
    }
    .stButton > button:hover {
        border-color: #2575fc;
        color: #2575fc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Choices ----------
PERSONALITIES = {
    "😂 Funny": "You are a funny AI agent.",
    "🎓 Teacher": "You are a patient teacher who explains things simply, with examples.",
    "🏴‍☠️ Pirate": "You are a pirate. Speak like one while still being helpful.",
    "💼 Professional": "You are a concise, professional assistant.",
    "🧘 Calm coach": "You are a calm, encouraging coach who gives motivating advice.",
    "😡 Angry coach": "You are an angry AI agent. You respond aggressively and impatiently."
}

MODELS = ["ministral-8b-2512", "mistral-small-latest", "mistral-large-latest"]

SUGGESTIONS = [
    "Tell me a joke",
    "Explain recursion simply",
    "Give me a study tip",
]

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    personality = st.radio("Personality", list(PERSONALITIES.keys()))
    model_name = st.selectbox("Model", MODELS)
    temperature = st.slider("Creativity", 0.0, 1.0, 0.7, 0.05)
    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

# ---------- State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Header ----------
st.markdown(
    f"""
    <div class="hero">
        <h1>🤖 Chatty</h1>
        <p>Currently in <b>{personality}</b> mode</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Suggestion buttons (only on an empty chat) ----------
clicked = None
if not st.session_state.messages:
    st.caption("Try one of these to get started:")
    cols = st.columns(len(SUGGESTIONS))
    for col, text in zip(cols, SUGGESTIONS):
        if col.button(text):
            clicked = text

# ---------- Show history ----------
for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role, avatar="🧑" if role == "user" else "🤖"):
        st.write(msg.content)

# ---------- Input ----------
prompt = st.chat_input("Type your message...") or clicked

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    model = ChatMistralAI(model=model_name, temperature=temperature)
    full_history = [SystemMessage(content=PERSONALITIES[personality])] + st.session_state.messages

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                response = model.invoke(full_history)
                st.write(response.content)
                st.session_state.messages.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.session_state.messages.pop()