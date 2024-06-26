import logging
import random

import sentry_sdk
import streamlit as st

from mbti import MBTI_DICT
from utils.discord_util import send_discord_message
from utils.openai_util import request_chat_completion
from utils.streamlit_util import write_common_style
from utils.streamlit_util import write_page_config
from utils.streamlit_util import write_sidebar
from utils.streamlit_util import write_streaming_response

sentry_sdk.init(
    dsn=st.secrets["SENTRY_KEY"],
    traces_sample_rate=0.01,
    profiles_sample_rate=0.01,
    environment=st.secrets["ENV"]
)

write_page_config()
write_common_style()
write_sidebar()
random_select = "랜덤으로 고르기"
options = [random_select] + [f"{k} ({MBTI_DICT[k]['persona']})" for k in sorted(MBTI_DICT.keys())]

if "counseling_results" not in st.session_state:
    st.session_state.counseling_results = {"results": []}

st.title("👂 MBTI 고민 상담실")
st.subheader("서로 다른 MBTI를 가진 AI들이 여러분들의 고민을 상담해줍니다!")
st.image("./images/banner.png")

auto_complete = st.toggle("예시로 채우기")
example_mbti = [random_select]
example_counsel = "썸남과 단둘이 인생네컷을 찍었어! 이거 그린라이트일까?"
with st.form("form"):
    selected_mbti_list = st.multiselect(
        label="상담받고 싶은 MBTI들을 3개 골라주세요",
        options=options,
        max_selections=3,
        default=example_mbti if auto_complete else []
    )
    question = st.text_area(
        label="여러분의 고민거리를 자세히 적어주세요.",
        placeholder=example_counsel,
        value=example_counsel if auto_complete else ""
    )
    submit_button = st.form_submit_button("제출")


if submit_button:
    if len(question) == 0:
        st.error("고민거리를 입력해주세요")
        st.stop()
    if len(selected_mbti_list) != 3 and random_select not in selected_mbti_list:
        st.error("상담받고 싶은 MBTI 3개를 선택해주세요.")
        st.stop()
    if random_select in selected_mbti_list:
        candidates = [x for x in options if x not in selected_mbti_list]
        selected_mbti_list.remove(random_select)
        random_mbti_list = random.sample(candidates, 3 - (len(selected_mbti_list)))
        selected_mbti_list += random_mbti_list
    st.success(f"{', '.join(selected_mbti_list)} 봇이 고민을 들어줍니다.")
    st.session_state.counseling_results["results"] = []
    selected_mbti_keys = [x.split(" ")[0] for x in selected_mbti_list]
    for i, mbti in enumerate(selected_mbti_keys):
        persona = MBTI_DICT[mbti]["persona"]
        counseling = MBTI_DICT[mbti]["counseling"]
        character = MBTI_DICT[mbti]["character"]
        system_role = f"""
당신은 유저의 친한 친구입니다. 
당신의 직업은 {persona}입니다.
당신의 성격은 {mbti}, {character}입니다.
친구의 고민을 들어줄 때 당신은 {counseling}
        """.strip()
        prompt = f"""
당신의 직업, 성격, 고민을 들어줄 때의 특징을 참고하여 유저의 고민을 상담해주세요.
반드시 반말로 친근하게 작성해주세요.
반드시 100단어 이내로 작성해주세요.
자신에 대한 소개는 하지 마세요.
이모지를 적절하게 사용해주세요.
---
유저의 고민: {question}
---
        """
        with st.expander(f"**{mbti} - {character}**", expanded=True):
            col1, col2 = st.columns([0.25, 0.75])
            with col1:
                st.image(f"./images/profile/{mbti}.png")
            with col2:
                try:
                    response = request_chat_completion(
                        system_role=system_role,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    message = write_streaming_response(response)
                    st.session_state.counseling_results["results"].append({
                        "mbti": mbti,
                        "message": message
                    })
                except Exception as e:
                    logging.error(e)
                    st.error("대화를 생성하는데 실패했습니다. 잠시 뒤에 다시 시도해주세요 🙇")
    send_discord_message(
        message_type="mbti 고민상담",
        message=f"고민: {question}"
    )
    st.stop()

if not st.session_state.counseling_results["results"]:
    st.stop()

for counseling_result in st.session_state.counseling_results["results"]:
    mbti = counseling_result["mbti"]
    message = counseling_result["message"]
    character = MBTI_DICT[mbti]["character"]
    with st.expander(f"**{mbti} - {character}**", expanded=True):
        col1, col2 = st.columns([0.25, 0.75])
    with col1:
        st.image(f"./images/profile/{mbti}.png")
    with col2:
        st.markdown(message)
