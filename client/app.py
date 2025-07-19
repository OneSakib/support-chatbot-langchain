import streamlit as st
import requests
import time

# Replace with your FastAPI server address
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Web Chat", layout="wide")
st.title("🌐 Website QA Chatbot")

# ---- Step 1: Submit a Website URL ----
st.subheader("Step 1: Enter Website URL")
url = st.text_input("Website URL", placeholder="https://example.com")
submit = st.button("Submit URL and Start Embedding")

if submit and url:
    with st.spinner("Submitting URL and generating embeddings..."):
        res = requests.post(f"{BACKEND_URL}/process-url", json={"url": url})
        if res.status_code == 200:
            task_id = res.json()["task_id"]
            project_id = res.json()["project_id"]
            st.success(f"Task submitted! Task ID: {task_id}")
            st.session_state["task_id"] = task_id
            st.session_state["project_id"] = project_id
        else:
            st.error("Failed to submit URL.")

# ---- Step 2: Poll task status ----
if "task_id" in st.session_state:
    st.subheader("Step 2: Embedding Status")
    task_id = st.session_state["task_id"]
    project_id = st.session_state["project_id"]

    status_placeholder = st.empty()
    while True:
        status_res = requests.get(f"{BACKEND_URL}/task-status/{task_id}")
        status = status_res.json().get("state", "UNKNOWN")
        status_placeholder.info(f"Task Status: {status}")
        if status in ["SUCCESS", "FAILURE"]:
            break
        time.sleep(2)

    if status == "SUCCESS":
        st.success("Embedding completed successfully!")
        st.session_state["ready"] = True
    else:
        st.error("Embedding failed.")

# ---- Step 3: Chat Interface ----
if st.session_state.get("ready"):
    st.subheader("Step 3: Chat with Your Website 🧠")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_input = st.text_input(
        "Ask a question", placeholder="What is this website about?")
    if st.button("Send") and user_input:
        st.session_state.chat_history.append(("user", user_input))

        res = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "message": user_input,
                "project_id": st.session_state["project_id"]
            },
        )
        if res.status_code == 200:
            answer = res.json()["response"]
            st.session_state.chat_history.append(("bot", answer))
        else:
            st.session_state.chat_history.append(
                ("bot", "Failed to get response."))

    # Display chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Bot:** {msg}")
