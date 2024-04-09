import openai
import streamlit as st

openai_client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def request_chat_completion(messages, system_role=None):
    if system_role:
        messages = [{"role": "system", "content": system_role}] + messages
    response = openai_client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        stream=True,
        timeout=3
    )
    return response
