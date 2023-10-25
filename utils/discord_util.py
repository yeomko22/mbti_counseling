import json

import requests
import streamlit as st


def send_discord_message(message_type, message):
    url = st.secrets["DISCORD_WEBHOOK_URL"]
    headers = {"Content-Type": "application/json"}
    data = {"content": f"유형: {message_type}\n{message}"}
    requests.post(url, headers=headers, data=json.dumps(data))
