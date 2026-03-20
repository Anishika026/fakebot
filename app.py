import streamlit as st
import requests
import datetime

st.set_page_config(page_title="Neuro Cybersecurity AI", layout="wide")

# ---------------------- SIMPLE MINIMAL STYLE ----------------------
st.markdown("""
<style>
/* Center title container */
.title-container {
    text-align: center;
    margin-top: 120px;
    margin-bottom: 40px;
}

/* Main title */
.main-title {
    font-family: 'Arial Black', sans-serif;
    font-size: 80px;
    font-weight: 900;
    color:grey;
    letter-spacing: 6px;
    text-transform: uppercase;
}

/* Sub title */
.sub-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 22px;
    color: #9aa4af;
    letter-spacing: 3px;
    margin-top: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="title-container">
    <div class="main-title">NEURO SHIELD</div>
    <div class="sub-title">AI Powered Cybersecurity Intelligence</div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@300;400;500&display=swap');

/* MAIN BACKGROUND */

.stApp {
    background-color: #0b1a2a;
    color: white;
    font-family: 'Inter', sans-serif;
}

/* HEADER */

.header {
    text-align:center;
    margin-top:20px;
}

.title {
    font-size:48px;
    font-weight:700;
    color:white;
    font-family:'Orbitron', sans-serif;
}

.subtitle{
    font-size:14px;
    color:#9aa4af;
    letter-spacing:2px;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:#0b1a2a;
}

/* SIDEBAR BUTTON */

.stButton button{
    background:#14283b;
    color:white;
    border:none;
    border-radius:6px;
    padding:10px;
    width:100%;
    text-align:left;
    font-size:15px;
}

.stButton button:hover{
    background:#14283b;
    color:white;
}

/* CHAT BUBBLES */

.user-bubble{
    background:#2f3944;
    color:white;
    padding:12px;
    border-radius:12px;
    max-width:70%;
    margin-left:auto;
    margin-top:10px;
}

.ai-bubble{
    background:#16293b;
    color:white;
    padding:12px;
    border-radius:12px;
    max-width:70%;
    margin-top:10px;
}

small{
color:#9aa4af;
font-size:11px;
}

/* CHAT INPUT */

[data-testid="stChatInput"]{
background:#14283b;
border:none;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Add grey border to sidebar */
[data-testid="stSidebar"] {
    border-right: 2px solid #9aa4af;  /* grey border */
}

/* Optional: adjust padding so content doesn’t touch the border */
[data-testid="stSidebar"] > div {
    padding-right: 10px;
}
</style>
""", unsafe_allow_html=True)





st.markdown("""
<style>

/* Entire page background */
html, body, .stApp {
    background-color: #061b2c !important;
}

/* Remove white block above header */
header {
    background-color: #061b2c !important;
}

/* Remove white block at bottom */
footer {
    background-color: #061b2c !important;
}

/* Main container */
section.main {
    background-color: #061b2c !important;
}

/* Block container padding fix */
.block-container {
    background-color: #061b2c !important;
}

</style>
""", unsafe_allow_html=True)






st.markdown("""
<style>

/* Whole page background */
.stApp{
    background-color:#061b2c;
}

/* Main app view */
[data-testid="stAppViewContainer"]{
    background-color:#061b2c;
}

/* Main content area */
[data-testid="stMain"]{
    background-color:#061b2c;
}

/* Bottom chat input container */
[data-testid="stBottomBlockContainer"]{
    background-color:#061b2c !important;
}

/* Chat input background */
[data-testid="stChatInput"]{
    background-color:#061b2c !important;
    padding-bottom:20px;
}

/* Remove default white padding */
.block-container{
    padding-bottom:0rem !important;
}

</style>
""", unsafe_allow_html=True)
# ---------------------- SIDEBAR ----------------------

with st.sidebar:


    if st.button("🗨    New Chat "):
        st.session_state.messages = []

    if st.button("🕘  Chat History"):
        st.session_state.page = "history"

    if st.button("🤖 AI Model Info"):
        st.session_state.page = "model"

    if st.button("⚙ Settings"):
        st.session_state.page = "settings"

    

    page = st.session_state.get("page", "chat")
    

        #-------------------------------------------------

st.markdown("""
<style>

/* Main page background */
.stApp {
    background-color: #071c2f;
}

/* Sidebar background */
[data-testid="stSidebar"]{
    background-color: #031423;
}

/* Sidebar buttons */
[data-testid="stSidebar"] button{
    background-color:#0d2a44;
    color:white;
    border-radius:8px;
}

/* Sidebar button hover */
[data-testid="stSidebar"] button:hover{
    background-color:#154a78;
}

/* Heading style */
.main-title{
    text-align:center;
    font-size:60px;
    font-weight:700;
    color:white;
    letter-spacing:3px;
}

/* Sub heading style */
.sub-title{
    text-align:center;
    font-size:18px;
    color:#9aa4af;
    letter-spacing:2px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------- PAGE STATE ----------------------

page = st.session_state.get("page", "chat")

# ---------------------- MODEL INFO PAGE ----------------------

if page == "model":

    st.subheader("AI Model Information")

    st.write("**Model Name:** Mistral")

    st.write("**Provider:** Ollama")

    st.write("**Capabilities:**")

    st.markdown("""
    • Threat Analysis  
    • Malware Detection  
    • Vulnerability Assessment  
    • Network Security Advice  
    • OWASP Top 10 Guidance  
    • Incident Response Assistance
    """)

    st.write("**Context Length:** 8K Tokens")
    st.write("**Temperature:** 0.7")
    st.write("**Top-p:** 0.9")

# ---------------------- SETTINGS PAGE ----------------------

elif page == "settings":

    st.subheader("Chatbot Settings")

    temperature = st.slider("Model Temperature",0.0,1.0,0.7)

    max_tokens = st.slider("Max Tokens",100,2000,1024)

    theme = st.selectbox(
        "Theme",
        ["Default Dark","Cyber Blue","Minimal"]
    )

    st.button("Save Settings")

# ---------------------- CHAT STORAGE ----------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------- CHAT DISPLAY ----------------------

for message in st.session_state.messages:

    timestamp = message["time"]

    if message["role"] == "user":

        st.markdown(
        f'<div class="user-bubble">{message["content"]}<br><small>{timestamp}</small></div>',
        unsafe_allow_html=True)

    else:

        st.markdown(
        f'<div class="ai-bubble">{message["content"]}<br><small>{timestamp}</small></div>',
        unsafe_allow_html=True)

# ---------------------- CHAT INPUT ----------------------

prompt = st.chat_input("Ask a cybersecurity question...")

if prompt:

    time_now = datetime.datetime.now().strftime("%H:%M")

    st.session_state.messages.append(
        {"role":"user","content":prompt,"time":time_now}
    )

    st.markdown(
    f'<div class="user-bubble">{prompt}<br><small>{time_now}</small></div>',
    unsafe_allow_html=True)

    with st.spinner("Thinking..."):

        system_prompt = "You are a professional cybersecurity expert assistant."

        full_prompt = system_prompt + "\nUser:" + prompt

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model":"mistral","prompt":full_prompt,"stream":False}
        )

        result = response.json()["response"]

    time_now = datetime.datetime.now().strftime("%H:%M")

    st.session_state.messages.append(
        {"role":"assistant","content":result,"time":time_now}
    )

    st.markdown(
    f'<div class="ai-bubble">{result}<br><small>{time_now}</small></div>',
    unsafe_allow_html=True)

# ---------------------- DASHBOARD ----------------------

st.divider()

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("⚠ Detected Threats Today","124")

with col2:
    st.metric("🛡 Blocked Attacks","87")

with col3:
    st.metric("📡Active Security Alerts","23")

  