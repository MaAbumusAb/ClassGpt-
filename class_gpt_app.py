import streamlit as st
import openai
import os

# Set up page configuration
st.set_page_config(page_title="ClassGPT – AI Study Assistant", layout="centered")

# Load OpenAI API key securely from environment variable
openai.api_key = os.getenv("sk-e0bd33139597474f893e0a212a7e39aa")

# App Title
st.markdown("## 📚 ClassGPT – Your Smart Study Assistant")
st.markdown("Explain any topic, generate quiz questions, or get summaries in English, Hausa, or Arabic!")

# Sidebar for language and task settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    language = st.selectbox("Choose Output Language", ["English", "Hausa", "Arabic"])
    task = st.selectbox("Select Task", ["Explain It", "Generate Quiz", "Summarize Topic"])
    st.markdown("💡 Try topics like *Photosynthesis*, *The Internet*, or *Algebra*.")

# Main input section
topic = st.text_input("✍️ Enter a topic you wil like to study:")

if st.button("Get Response") and topic:
    st.markdown("⏳ Processing... Please wait.")

    # Dynamic prompt based on task and language
    prompt_map = {
        "Explain It": f"Explain the topic '{topic}' in simple terms, in {language}.",
        "Generate Quiz": f"Create one quiz question on the topic '{topic}' in {language}.",
        "Summarize Topic": f"Summarize the topic '{topic}' concisely in {language}."
    }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and multilingual AI tutor for students."},
                {"role": "user", "content": prompt_map[task]}
            ]
        )
        result = response['choices'][0]['message']['content']

        st.success("✅ Here's your result:")
        st.write(result)
        st.code(result, language='markdown')

        st.markdown("---")
        st.markdown("> 💡 *“Education is the passport to the future, for tomorrow belongs to those who prepare for it today.”*")

    except Exception as e:
        st.error("An error occurred. Please check your API key and internet connection.")
        st.text(str(e))
else:
    st.info("Enter a topic and click 'Get Response' to begin learning.")
