import os
import subprocess
import sys
import streamlit as st
from google import genai
from google.genai import types

def judicial_chatbot(user_input):
    client = genai.Client(
        api_key="AIzaSyBoCiFMnGRwGy5XHbdEeggiE7RTe865usg"
    )

    model = "gemini-3-flash-preview"

    system_prompt = """
You are a Judicial Court Process & Case Flow Explainer Bot.

Your role is to explain judicial court systems, procedures, and legal concepts
in a general, procedural, and educational manner only.

You are NOT a lawyer, judge, or legal advisor.

You may explain:
- Court structure and purpose
- Case lifecycle and stages
- Court hearings and procedures
- Legal terminology in simple language
- Roles of judges, lawyers, and court staff
- Appeals and post-judgment concepts (high-level)
- Court etiquette and public awareness

You MUST NOT:
- Give legal advice
- Predict case outcomes
- Suggest legal strategies
- Interpret legal notices
- Draft or review legal documents
- Recommend lawyers
- Answer unrelated questions

If the user asks for legal advice or case-specific guidance, respond EXACTLY with:
"⚠️ I can only explain general judicial procedures and legal concepts. I cannot provide legal advice, opinions, case-specific guidance, or outcome predictions."

If the user asks an invalid or unrelated question, respond EXACTLY with:
"❌ Invalid question. This assistant only provides information related to judicial court systems, procedures, and legal terminology."
"""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=system_prompt + "\n\nUser Question:\n" + user_input
                )
            ]
        )
    ]

    config = types.GenerateContentConfig(
        temperature=0.3,
        max_output_tokens=512
    )

    response_text = ""

    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config
        ):
            if chunk.text:
                response_text += chunk.text
    except Exception as e:
        response_text = f"ERROR: {e}"

    return response_text

st.set_page_config(
    page_title="JudicialProcessExplainer",
    page_icon="⚖️",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.shutterstock.com/search/courtroom-background");
        background-size: cover;
        background-attachment: fixed;
    }

    .chat-box {
        background-color: #ffffff;
        color: #000000;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        font-size: 16px;
        line-height: 1.6;
    }

    .user {
        font-weight: bold;
        color: #1a1a1a;
    }

    .bot {
        color: #2b2b2b;
    }

    .title {
        color: #ffffff;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.9);
    }

    input, textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    button {
        background-color: #2c2c2c !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 class='title'>⚖️ Judicial Process Explainer</h1>", unsafe_allow_html=True)
st.markdown("<p class='title'>Understand court procedures clearly and ethically</p>", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask a question about judicial court procedures")

if st.button("Send") and user_input.strip():
    st.session_state.chat.append(("You", user_input))
    reply = judicial_chatbot(user_input)
    st.session_state.chat.append(("Bot", reply))

for role, msg in st.session_state.chat:
    if role == "You":
        st.markdown(
            f"<div class='chat-box'><span class='user'>You:</span> {msg}</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div class='chat-box'><span class='bot'>Bot:</span> {msg}</div>",
            unsafe_allow_html=True
        )

st.markdown(
    "<div class='chat-box'><b>⚠️ Disclaimer:</b> This assistant provides general information only and does not offer legal advice.</div>",
    unsafe_allow_html=True
)
