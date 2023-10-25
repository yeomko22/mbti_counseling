import streamlit as st
from sentry_sdk import capture_message
import sentry_sdk


def init_sentry():
    if 'sentry_initialized' not in st.session_state:
        sentry_sdk.init(
            dsn=st.secrets["SENTRY_KEY"],
            traces_sample_rate=0.01,
            profiles_sample_rate=0.01,
            environment=st.secrets["ENV"]
        )
        st.session_state.sentry_initialized = True


def capture_exception_message(e):
    init_sentry()
    capture_message(e)
