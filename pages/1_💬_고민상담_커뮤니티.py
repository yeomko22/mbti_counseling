import random

import streamlit as st

from mbti import MBTI_DICT
from utils.openai_util import request_chat_completion
from utils.streamlit_util import write_streaming_response, write_common_style


