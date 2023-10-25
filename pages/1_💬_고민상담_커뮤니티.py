import logging
import math

import streamlit as st

from mbti import MBTI_DICT
from utils.streamlit_util import write_common_style, write_page_config, write_sidebar, nav_page
from utils.supabase_util import count_records, read_page

write_page_config()
write_common_style()
write_sidebar()

st.title("💬 고민상담 커뮤니티")
st.subheader("MBTI들이 상담해준 결과를 공유해봐요!")
nav_button = st.button("다시 고민상담하러 가기")
if nav_button:
    nav_page(page_name="")
st.markdown("""
<style>
.streamlit-expanderHeader p {
    font-size: 17px;
}
.streamlit-expanderContent h3 {
    font-weight: bold;
    font-size: 20px;
}
[data-testid="stButton"] {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)


if "counseling_results" in st.session_state:
    del st.session_state["counseling_results"]
if "page" not in st.session_state:
    st.session_state.page = 1

pagesize = 10
with st.spinner("고민 상담 데이터를 읽어오고 있습니다..."):
    try:
        count = count_records(target_table="counseling")
        data = read_page(
            target_table="counseling",
            last_id=(count - pagesize * (st.session_state.page - 1) + 1)
        )
    except Exception as e:
        logging.error(e)
        st.error("데이터를 읽어오지 못했습니다. 잠시 뒤에 다시 시도해주세요.")
        st.stop()


total_pages = math.ceil(count / pagesize)
if data:
    st.session_state.last_id = data[-1]["id"]

for item in data:
    question = item["question"]
    header_question = question
    header_limit = 30
    if len(header_question) > header_limit:
        header_question = header_question[:header_limit - 3] + "..."
    with st.expander(f"{item['id']}\.**{item['nickname']}**의 {item['counseling_type'].split(' ')[0]} 고민 &nbsp;&nbsp;&nbsp; {header_question}"):
        st.subheader(f"{question}")
        counseling_items = item["answer"]["results"]
        for counseling_item in counseling_items:
            mbti = counseling_item["mbti"]
            message = counseling_item["message"]
            character = MBTI_DICT[mbti]["character"]
            col1, col2 = st.columns([0.25, 0.75])
            with col1:
                st.image(f"./images/profile/{mbti}.png")
            with col2:
                st.markdown(f"**{mbti}의 생각**")
                st.markdown(message)
        st.markdown(f"""**{item["nickname"]}**님의 의견  
{item["comment"]}        
""")


def change_page():
    selected_page = int(st.session_state["select_page"].split(" / ")[0])
    st.session_state.page = selected_page


cols = st.columns(3)
with cols[1]:
    st.selectbox(
        label="페이지",
        label_visibility="collapsed",
        options=[f"{x+1} / {total_pages} 페이지" for x in range(total_pages)],
        index=st.session_state.page - 1,
        on_change=change_page,
        key="select_page"
    )
