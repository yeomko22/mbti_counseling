import streamlit as st


def write_streaming_response(response):
    placeholder = st.empty()
    message = ""
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message + "▌")
        else:
            break
    placeholder.markdown(message)
    return message


def write_sidebar():
    with st.sidebar:
        st.markdown("")
        st.markdown("")
        st.markdown("Powered by gpt-3.5-turbo")
        st.markdown("""
    **Youtube**: [퍼스트펭귄 코딩스쿨](https://www.youtube.com/channel/UCUFk9scQ-SqP993DRC4z_fA)  
    **Blog**: https://blog.firstpenguine.school   
    **Email**: hyeongjun.kim@firstpenguine.school
    """)


def write_common_style():
    st.markdown("""
    <style>
    [data-testid="column"] img {
        border-radius: 50%;
        border: 1px solid #d2d2d2;
        filter: drop-shadow(3px 3px 5px #d2d2d2);
    }
    h1 {
        text-align: center;
    }
    h3 {
        text-align: center;
        font-size: 18px;
        font-weight: normal;
    }
    [data-testid="StyledFullScreenButton"] {
        visibility: hidden;
    }
    [data-testid="block-container"] {
        padding: 2em;
    }
    div {
        justify-content: center;
    }
    [data-testid="stCheckbox"] div {
        justify-content: left;
    }
    [data-testid="stMultiSelect"] div {
        justify-content: left;
    }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    [data-testid="StyledLinkIconContainer"] {
        pointer-events: none;
    }
    img {
        max-height: 250px;
    }
    </style>
    """, unsafe_allow_html=True)


def write_page_config():
    st.set_page_config(
        page_icon="👂",
        page_title="MBTI 고민상담실",
    )


def clear_session_state(cur_chapter: str = None):
    for k in st.session_state.keys():
        if k == cur_chapter:
            continue
        del st.session_state[k]


def write_sidebar():
    with st.sidebar:
        st.markdown("Powered by gpt-3.5-turbo")
        st.markdown("""
        **Youtube**: [퍼스트펭귄 코딩스쿨](https://www.youtube.com/channel/UCUFk9scQ-SqP993DRC4z_fA)  
        **Blog**: https://blog.firstpenguine.school   
        **Email**: hyeongjun.kim@firstpenguine.school
        """)
