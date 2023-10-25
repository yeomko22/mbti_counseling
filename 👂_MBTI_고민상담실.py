import random

import streamlit as st

from mbti import MBTI_DICT
from utils.openai_util import request_chat_completion
from utils.streamlit_util import write_streaming_response, write_common_style, write_page_config

write_page_config()
write_common_style()
random_select = "랜덤으로 3개 고르기"
options = [random_select] + [f"{k} ({MBTI_DICT[k]['persona']})" for k in sorted(MBTI_DICT.keys())]

if "counseling_results" not in st.session_state:
    st.session_state.counseling_results = [None, None, None]

st.title("👂 MBTI 고민 상담실")
st.subheader("서로 다른 MBTI를 가진 AI들이 여러분들의 고민을 상담해줍니다!")
st.image("./images/banner.png")

auto_complete = st.toggle("예시로 채우기")
example_mbti = [random_select]
example_counsel = "썸남과 단둘이 인생네컷을 찍었어! 근데 이거 그린라이트일까...?"
with st.form("form"):
    selected_mbti_list = st.multiselect(
        label="상담받고 싶은 MBTI들을 3개 골라주세요",
        options=options,
        max_selections=3,
        default=example_mbti if auto_complete else []
    )
    input_text = st.text_area(
        label="여러분의 고민거리를 자세히 적어주세요.",
        placeholder=example_counsel,
        value=example_counsel if auto_complete else ""
    )
    submit_button = st.form_submit_button("제출")


def share_form():
    with st.form("share_form", clear_on_submit=True):
        cols = st.columns([0.2, 0.8])
        with cols[0]:
            nickname = st.text_input(
                label="닉네임(선택)",
                placeholder="익명의 고민러",
                value="익명의 고민러"
            )
        with cols[1]:
            comment = st.text_input(
                label="댓글",
                placeholder="ENFP 봇의 조언이 도움이 됐어요!"
            )
        share_submit = st.form_submit_button(
            "💬 커뮤니티에 공유하기",
        )
        if share_submit:
            st.toast("공유 완료! 커뮤니티에서 확인해보세요.", icon="✅")


if submit_button:
    if len(input_text) == 0:
        st.error("고민거리를 입력해주세요")
        st.stop()
    if len(selected_mbti_list) != 3 and random_select not in selected_mbti_list:
        st.error("상담받고 싶은 MBTI 3개를 선택해주세요.")
        st.stop()
    if random_select in selected_mbti_list:
        selected_mbti_list = random.sample(options[1:], 3)
        st.success(f"랜덤하게 선택한 {', '.join(selected_mbti_list)} 봇이 고민을 들어줍니다.")
    else:
        st.success(f"{', '.join(selected_mbti_list)} 봇이 고민을 들어줍니다.")
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
반드시 80자 이상 작성해주세요.
반드시 100자 이내로 작성해주세요.
이모지를 적절하게 사용해주세요.
---
유저의 고민: {input_text}
---
        """
        with st.expander(f"**{mbti} - {character}**", expanded=True):
            col1, col2 = st.columns([0.25, 0.75])
            with col1:
                st.image(f"./images/profile/{mbti}.png")
            with col2:
                response = request_chat_completion(
                    system_role=system_role,
                    messages=[{"role": "user", "content": prompt}]
                )
                message = write_streaming_response(response)
                st.session_state.counseling_results[i] = {
                    "mbti": mbti,
                    "message": message
                }
    share_form()
    st.stop()

if st.session_state.counseling_results[0]:
    for counseling_result in st.session_state.counseling_results:
        if not counseling_result:
            continue
        mbti = counseling_result["mbti"]
        message = counseling_result["message"]
        character = MBTI_DICT[mbti]["character"]
        with st.expander(f"**{mbti} - {character}**", expanded=True):
            col1, col2 = st.columns([0.25, 0.75])
        with col1:
            st.image(f"./images/profile/{mbti}.png")
        with col2:
            st.markdown(message)
    share_form()
