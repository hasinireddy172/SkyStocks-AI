import streamlit as st
from agent import run_agent

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="SkyStocks AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background: linear-gradient(
        135deg,
        #eef6ff 0%,
        #f5f9ff 50%,
        #eefaf5 100%
    );
}

/* Main container */
.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Sidebar */
ssection[data-testid="stSidebar"] {
    background: rgba(248, 251, 255, 0.95);
    border-right: 1px solid #dbe5ef;
}
/* Logo */
.logo {
    font-size: 27px;
    font-weight: 700;
    margin-bottom: 5px;
}

.logo-subtitle {
    color: #64748b;
    font-size: 14px;
}

/* Hero */
.hero {
    text-align: center;
    padding: 55px 20px 30px 20px;
}

.hero-title {
    font-size: 46px;
    font-weight: 750;
    margin-bottom: 12px;
}

.hero-subtitle {
    color: #64748b;
    font-size: 18px;
}

/* Tool cards */
.tool-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    min-height: 150px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.tool-icon {
    font-size: 32px;
    margin-bottom: 10px;
}

.tool-title {
    font-size: 18px;
    font-weight: 650;
}

.tool-description {
    color: #64748b;
    font-size: 14px;
    margin-top: 8px;
}

/* Response */
.response-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 25px;
    margin-top: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.response-title {
    font-size: 18px;
    font-weight: 650;
    margin-bottom: 12px;
}

/* Input */
div[data-testid="stChatInput"] {
    margin-top: 20px;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}

/* Divider */
.divider {
    height: 1px;
    background: #e5e7eb;
    margin: 25px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("""
    <div class="logo">🌐 SkyStocks AI</div>
    <div class="logo-subtitle">
        Weather & Market Intelligence
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Available Tools")

    st.markdown("""
    🌤️ **Weather**

    Get current weather information.

    📈 **Stock Analysis**

    Get stock market information.

    """)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.caption("Powered by Gemini API")


# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="hero">

<div class="hero-title">
    AI That Can Take Action
</div>

<div class="hero-subtitle">
    Ask a question and let the AI choose the right tool.
</div>

</div>
""", unsafe_allow_html=True)


# =========================
# TOOL CARDS
# =========================

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🌤️</div>
        <div class="tool-title">Weather</div>
        <div class="tool-description">
            Get real-time weather information for a city.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">📈</div>
        <div class="tool-title">Stock Market</div>
        <div class="tool-description">
            Retrieve stock prices and market data.
        </div>
    </div>
    """, unsafe_allow_html=True)



# =========================
# CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input(
    "Ask SkyStocks AI anything..."
)


# =========================
# PROCESS QUERY
# =========================

if prompt:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("🤖 Agent is working..."):

            result = run_agent(prompt)

        st.write(result)

    # Store response
    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

