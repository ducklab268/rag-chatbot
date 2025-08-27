import streamlit as st
from backend import get_answer, build_index

# Build FAISS index at startup
try:
    build_index()
except Exception as e:
    st.warning(f"⚠️ Index build skipped: {e}")

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("📚 Your Personal Knowledge Chatbot")
st.write("Ask me anything based on your uploaded knowledge base (`blogs/` folder).")

if "history" not in st.session_state:
    st.session_state.history = []

user_query = st.text_input("🔍 Enter your question:")

if st.button("Get Answer"):
    if user_query.strip():
        with st.spinner("🤔 Thinking..."):
            answer = get_answer(user_query)
        st.session_state.history.append((user_query, answer))
    else:
        st.warning("Please enter a question first.")

# Display chat history
for q, r in reversed(st.session_state.history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {r}")
