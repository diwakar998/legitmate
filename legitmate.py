# landing_app.py
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Landing Page + Chat", layout="wide")

# ---------------- Session state ----------------
if "active_page" not in st.session_state:
    st.session_state.active_page = "Welcome"
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list[dict]: {"role":"user/assistant","text":...}

# ---------------- Styles ----------------
st.markdown("""
<style>
/* Page background + text */
.stApp {
  background: radial-gradient(1100px 600px at 20% -5%, #ffffff 0%, #f8fbff 70%, #eff4fa 100%);
}

/* Left navigation card */
.nav-card {
  background: #fff;
  border: 1px solid #e6ecf3;
  border-radius: 16px;
  padding: 14px 14px;
  box-shadow: 0 10px 26px rgba(16,38,73,.06);
}

/* Right content card */
.content-card {
  background: #fff;
  border: 1px solid #e6ecf3;
  border-radius: 16px;
  padding: 20px 22px;
  min-height: 420px;
  box-shadow: 0 12px 30px rgba(16,38,73,.06);
}

/* Floating chat container (button + window) */
.chat-float {
  position: fixed;
  right: 20px;
  bottom: 20px;
  width: 360px;     /* chat window width */
  z-index: 9999;
}

/* When closed, only the button shows; we keep width small for the icon */
.chat-float.closed { width: 70px; }

/* Chat window panel */
.chat-panel {
  background: #ffffff;
  border: 1px solid #e6ecf3;
  border-radius: 16px;
  padding: 10px 12px 12px 12px;
  margin-bottom: 10px;
  box-shadow: 0 14px 36px rgba(16,38,73,.12);
}

/* Chat header row */
.chat-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 4px 2px 10px 2px; border-bottom: 1px solid #eef2f8; margin-bottom: 10px;
}

/* Scrollable chat messages area */
.chat-body {
  height: 250px;
  overflow-y: auto;
  padding-right: 4px;
}

/* Message bubbles */
.msg {
  padding: 8px 12px; border-radius: 12px; margin: 6px 0; width: fit-content; max-width: 90%;
}
.msg.user { background: #eef6ff; margin-left: auto; }
.msg.bot  { background: #f6f7fb; margin-right: auto; }

/* Round floating button container */
.fab {
  display: flex; justify-content: flex-end;
}

/* Make Streamlit button fill our custom width when needed */
.stButton>button { width: 100%; border-radius: 999px; }

/* Small icon button */
.small-icon > button {
  width: 56px; height: 56px; border-radius: 50%;
  font-size: 22px;
  box-shadow: 0 10px 20px rgba(16,38,73,.18);
}

/* Inputs in chat footer */
.chat-input-row { display: flex; gap: 6px; }
.chat-input-row .element-container { flex: 1; }
</style>
""", unsafe_allow_html=True)

# ---------------- Navigation (Left) & Content (Right) ----------------
left, right = st.columns([1, 2], gap="large")

with left:
    st.markdown("<div class='nav-card'>", unsafe_allow_html=True)
    st.subheader("Navigation")
    # Your left-pane "links"
    pages = ["Welcome", "About", "Products", "Contact"]
    choice = st.radio(" ", pages, index=pages.index(st.session_state.active_page), label_visibility="collapsed")
    st.session_state.active_page = choice
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.subheader(st.session_state.active_page)

    # Render content for the selected link
    if st.session_state.active_page == "Welcome":
        st.write("This is your landing page. Pick a link on the left to see more.")
        st.write("- Quick updates, announcements, or hero section can live here.")
    elif st.session_state.active_page == "About":
        st.write("We help teams adopt Agentic AI safely and effectively.")
        st.markdown("- **Mission:** Deliver measurable productivity with AI\n- **Focus:** Readiness, governance, and impact")
    elif st.session_state.active_page == "Products":
        st.write("A few highlights:")
        st.markdown("1. Readiness Questionnaire\n2. Agentic Copilots\n3. Analytics & Dashboards")
    elif st.session_state.active_page == "Contact":
        st.markdown("**Email:** hello@example.com  \n**Support:** support@example.com  \n**Office:** Berlin, DE")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Floating Chat (icon + panel) ----------------
# We render this LAST so it's on top of everything (higher z-index)
placeholder = st.empty()
with placeholder.container():
    # Wrapper div gives us fixed positioning via CSS
    st.markdown(f"<div class='chat-float {'closed' if not st.session_state.chat_open else ''}'>", unsafe_allow_html=True)

    if st.session_state.chat_open:
        # ---- Chat window ----
        st.markdown("<div class='chat-panel'>", unsafe_allow_html=True)
        st.markdown("""
            <div class='chat-header'>
                <div><strong>Assistant</strong></div>
                <div style="font-size:12px;color:#7489a6;">Mini chat · {}</div>
            </div>
        """.format(datetime.utcnow().strftime("%H:%M UTC")), unsafe_allow_html=True)

        # messages
        st.markdown("<div class='chat-body'>", unsafe_allow_html=True)
        # Render chat history
        for msg in st.session_state.chat_history:
            cls = "user" if msg["role"] == "user" else "bot"
            st.markdown(f"<div class='msg {cls}'>{msg['text']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # input row in a small form so Enter works
        with st.form("chat_form", clear_on_submit=True):
            cols = st.columns([1, 6, 2])
            with cols[1]:
                user_text = st.text_input("Type a message", label_visibility="collapsed")
            with cols[2]:
                send = st.form_submit_button("Send")

        # handle send
        if send and user_text.strip():
            st.session_state.chat_history.append({"role": "user", "text": user_text.strip()})
            # ---- Simple demo bot (replace with your LLM/API) ----
            reply = f"I heard: {user_text.strip()}"
            st.session_state.chat_history.append({"role": "assistant", "text": reply})
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        # Close button below the panel
        c = st.container()
        with c:
            st.button("Close chat", key="close_chat", on_click=lambda: st.session_state.update(chat_open=False))
    else:
        # ---- Floating round icon button only ----
        fab = st.container()
        with fab:
            st.markdown("<div class='fab'>", unsafe_allow_html=True)
            st.button("💬", key="open_chat", on_click=lambda: st.session_state.update(chat_open=True), help="Open chat", type="primary")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

