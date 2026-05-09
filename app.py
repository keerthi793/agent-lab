import streamlit as st
from agents.agent_graph import on_message_events

st.set_page_config(
    page_title="Keerthivasan A",
    page_icon=":sparkles:",
    # layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>

/* =========================================================
   IMPORT GOOGLE FONTS
========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&family=Open+Sans:wght@300;400;500;600&display=swap');


/* =========================================================
   GLOBAL APP
========================================================= */
.stApp {

    background: linear-gradient(
        135deg,
        #081120 0%,
        #0B1F3A 100%
    );

    color: #FFFFFF;

    font-family: 'Open Sans', sans-serif;
}


/* =========================================================
   MAIN CONTAINER
========================================================= */
.block-container {

    padding-top: 2rem;
    padding-bottom: 2rem;

    max-width: 1200px;
}


/* =========================================================
   TYPOGRAPHY
========================================================= */

/* Main Title */
h1 {

    font-family: 'Poppins', sans-serif;

    font-weight: 800;

    font-size: 3rem;

    letter-spacing: -1px;

    color: #FFFFFF;
}


/* Section Heading */
h2 {

    font-family: 'Poppins', sans-serif;

    font-weight: 700;

    font-size: 2rem;

    letter-spacing: -0.5px;

    color: #FFFFFF;
}


/* Subheading */
h3 {

    font-family: 'Poppins', sans-serif;

    font-weight: 600;

    color: #CBD5F5;
}


/* Paragraphs */
p {

    font-family: 'Open Sans', sans-serif;

    font-size: 1rem;

    line-height: 1.7;

    color: #CBD5F5;
}


/* =========================================================
   SIDEBAR
========================================================= */
section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #111827 0%,
        #0F172A 100%
    );

    border-right: 1px solid rgba(255,255,255,0.06);

    box-shadow:
        4px 0 24px rgba(0,0,0,0.18);

    backdrop-filter: blur(10px);
}


/* Sidebar Text */
section[data-testid="stSidebar"] * {

    color: #CBD5F5;
}


/* =========================================================
   BUTTONS
========================================================= */
.stButton > button {

    background: linear-gradient(
        135deg,
        #8B5CF6 0%,
        #7C3AED 100%
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 0.7rem 1.4rem;

    font-family: 'Poppins', sans-serif;

    font-weight: 600;

    transition: all 0.25s ease;

    box-shadow:
        0 4px 18px rgba(139, 92, 246, 0.25);
}


/* Button Hover */
.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 8px 24px rgba(139, 92, 246, 0.35);

    background: linear-gradient(
        135deg,
        #A78BFA 0%,
        #8B5CF6 100%
    );
}


/* =========================================================
   INPUT FIELDS
========================================================= */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {

    background-color: #163D57 !important;

    color: #FFFFFF !important;

    border-radius: 12px !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    font-family: 'Open Sans', sans-serif;
}


/* =========================================================
   METRIC CARDS
========================================================= */
[data-testid="stMetric"] {

    background: rgba(22, 61, 87, 0.75);

    border: 1px solid rgba(255,255,255,0.06);

    padding: 1.2rem;

    border-radius: 18px;

    backdrop-filter: blur(8px);

    box-shadow:
        0 4px 20px rgba(0,0,0,0.15);
}


/* =========================================================
   DATAFRAMES
========================================================= */
[data-testid="stDataFrame"] {

    border-radius: 16px;

    overflow: hidden;
}


/* =========================================================
   EXPANDERS
========================================================= */
.streamlit-expanderHeader {

    background-color: #163D57;

    border-radius: 12px;

    color: #FFFFFF;

    font-family: 'Poppins', sans-serif;

    font-weight: 600;
}


/* =========================================================
   TABS
========================================================= */
.stTabs [data-baseweb="tab-list"] {

    gap: 8px;
}


.stTabs [data-baseweb="tab"] {

    background-color: #163D57;

    border-radius: 10px;

    padding: 10px 18px;

    color: #CBD5F5;

    font-family: 'Poppins', sans-serif;

    font-weight: 500;
}


/* Active Tab */
.stTabs [aria-selected="true"] {

    background-color: #8B5CF6 !important;

    color: white !important;
}


/* =========================================================
   LINKS
========================================================= */
a {

    color: #A78BFA !important;

    text-decoration: none;
}


a:hover {

    color: #C4B5FD !important;
}


/* =========================================================
   SCROLLBAR
========================================================= */
::-webkit-scrollbar {

    width: 10px;
}


::-webkit-scrollbar-track {

    background: #081120;
}


::-webkit-scrollbar-thumb {

    background: #8B5CF6;

    border-radius: 10px;
}


/* =========================================================
   HORIZONTAL RULES
========================================================= */
hr {

    border: none;

    height: 1px;

    background: rgba(255,255,255,0.08);

    margin-top: 2rem;

    margin-bottom: 2rem;
}


/* =========================================================
   GLASS CARD CLASS
========================================================= */
.glass-card {

    background: rgba(22, 61, 87, 0.65);

    border: 1px solid rgba(255,255,255,0.06);

    border-radius: 20px;

    padding: 1.5rem;

    backdrop-filter: blur(12px);

    box-shadow:
        0 8px 32px rgba(0,0,0,0.18);
}


/* =========================================================
   SECTION LABELS
========================================================= */
.section-label {

    color: #A78BFA;

    text-transform: uppercase;

    letter-spacing: 1.5px;

    font-size: 0.8rem;

    font-family: 'Poppins', sans-serif;

    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

st.markdown("", text_alignment="center")
st.header("✦ Prompt Demo", text_alignment="center")

if 'final_state' not in st.session_state:
    st.session_state["final_state"] = {}

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

with st.sidebar:
    if st.button("Restart"):
        st.session_state['messages'] = []
        st.session_state['final_state'] = {}


async def stream_handler(input_message):
    async for event in on_message_events(input_message):
        print(event)
        if event['type'] == 'token':
            yield event['data']
        elif event['type'] == 'final_state':
            st.session_state["final_state"] = event["data"]


for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['text'], unsafe_allow_html=True)

if user_input := st.chat_input("Enter your message"):
    st.session_state['messages'].append({'role': 'user', 'text': user_input})
    with st.chat_message("user"):
        st.markdown(user_input, unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("Thinking.."):
            full_response = st.write_stream(stream_handler(user_input))

        st.session_state['messages'].append({'role': 'assistant', 'text': str(full_response)})
