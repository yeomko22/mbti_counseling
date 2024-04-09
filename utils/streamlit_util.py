import streamlit as st
from streamlit.components.v1 import html


def write_streaming_response(response):
    content = ""
    placeholder = st.empty()
    for part in response:
        if isinstance(part, str) or not part.id:
            continue
        delta = part.choices[0].delta
        if delta.content:
            content += delta.content
            placeholder.markdown(content + "▌")
    placeholder.markdown(content)
    return content



def write_sidebar():
    with st.sidebar:
        st.markdown("")
        st.markdown("")
        st.markdown("Powered by gpt-3.5-turbo")
        st.markdown("""
    [📺 퍼펭스쿨 유튜브](https://www.youtube.com/channel/UCUFk9scQ-SqP993DRC4z_fA)  
    [✍️ 퍼펭스쿨 블로그](https://blog.firstpenguine.school)
    [✉️ 이메일](hyeongjun.kim@firstpenguine.school)
    """)


def write_common_style():
    st.markdown("""
    <style>
    [data-testid="stAppViewBlockContainer"] {
        padding: 1rem 0rem 5rem 0rem;
    }
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
    [data-testid="stSidebarUserContent"] {
        padding: 1em;
    }
    [data-testid="stSidebarUserContent"] .block-container {
        padding: 0;
    }
    [data-testid="stMarkdownContainer"] a {
        text-decoration: none;
        color: black;
    }
    [data-testid="stMarkdownContainer"] a:hover {
        color: #FF4B4B;
    }
    section[data-testid="stSidebar"] {
        width: 200px !important;
    }
    [data-baseweb="popover"] li.st-g8 {
        visibility: hidden;
    }
    [data-baseweb="popover"] li.st-g8:before {
        content: "3개를 모두 선택했습니다!";
        visibility: visible;
    }
    </style>
    """, unsafe_allow_html=True)


def write_page_config():
    st.set_page_config(
        page_icon="👂",
        page_title="MBTI 고민상담실",
        initial_sidebar_state="collapsed"
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
[📺 퍼펭스쿨 유튜브](https://www.youtube.com/channel/UCUFk9scQ-SqP993DRC4z_fA)  
[✍️ 퍼펭스쿨 블로그](https://blog.firstpenguine.school)  
[✉️ 이메일](hyeongjun.kim@firstpenguine.school)  
         """)


def nav_page(page_name: str, timeout_secs: int = 3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                const collator = new Intl.Collator('ko');
                for (var i = 0; i < links.length; i++) {
                    uri = links[i].href.split("/").slice(-1)[0];
                    decoded_uri = decodeURI(uri);
                    const result = collator.compare(decoded_uri, page_name);
                    if (result === 0) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
        """ % (page_name, timeout_secs)
    html(nav_script)

