import streamlit as st
from openai import OpenAI
import os

# Set up page configuration
st.set_page_config(page_title="ClassGPT – AI Study Assistant", layout="centered")

# Initialize OpenAI client securely
client = OpenAI(api_key=os.getenv("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"))

# App Title
st.markdown("## 📚 ClassGPT – Your Smart Study Assistant")
st.markdown("Explain topics, generate quizzes, and get summaries in English, Hausa, or Arabic!")

# Sidebar settings
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    language = st.selectbox("Choose Output Language", ["English", "Hausa", "Arabic"])
    task = st.selectbox("Select Task", ["Explain It", "Generate Quiz", "Summarize Topic"])
    st.markdown("💡 Try topics like *Photosynthesis*, *The Internet*, or *Algebra*.")

# Main input section
topic = st.text_input("✍️ Enter a topic you’d like to study:")

if st.button("Get Response") and topic:
    st.markdown("⏳ Processing... Please wait...")

    # Prepare the prompt
    prompt_map = {
        "Explain It": f"Explain the topic '{topic}' in simple terms in {language}.",
        "Generate Quiz": f"Create one quiz question on the topic '{topic}' in {language}.",
        "Summarize Topic": f"Summarize the topic '{topic}' concisely in {language}."
    }
    prompt = prompt_map[task]

    try:
        # Make API request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, multilingual AI tutor."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and display the response
        output = response.choices[0].message.content
        st.success("✅ Here's your result:")
        st.write(output)
        st.code(output, language='markdown')

        st.markdown("---")
        st.markdown("> 💡 *“Education is the passport to the future, for tomorrow belongs to those who prepare for it today.”*")

    except Exception as e:
        st.error("An error occurred. Please check your API key or network.")
        st.text(str(e))

else:
    st.info("Enter a topic and click 'Get Response' to begin.")
