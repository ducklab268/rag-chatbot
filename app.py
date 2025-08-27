import streamlit as st
from backend import get_answer, build_index

st.set_page_config(page_title="📚 RAG Chatbot", page_icon="🤖")
st.title("📚 Your Personal Knowledge Chatbot")
st.write("Ask me anything based on your uploaded knowledge base (`blogs/` folder).")

# Build index at startup
try:
    build_index()
except Exception as e:
    st.warning(f"⚠️ Index build skipped: {e}")

user_query = st.text_input("🔍 Enter your question:")

if st.button("Get Answer"):
    if user_query.strip():
        with st.spinner("🤔 Thinking..."):
            try:
                answer = get_answer(user_query)
            except Exception as e:
                st.error(f"❌ Error: {e}")
                answer = None
        if answer:
            st.success("✅ Answer:")
            st.write(answer)
    else:
        st.warning("Please enter a question first.")
