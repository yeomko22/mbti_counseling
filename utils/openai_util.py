import openai
import streamlit as st


openai.api_key = st.secrets["OPENAI_API_KEY"]


def request_chat_completion(messages, system_role=None):
    if system_role:
        messages = [{"role": "system", "content": system_role}] + messages
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        timeout=3
    )
    return response
