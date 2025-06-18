import streamlit as st
import os
import requests
import json

# --- Configuration for Hugging Face LLaMA 3 Inference API ---
# IMPORTANT:
# Set these as environment variables BEFORE running your Streamlit app:
# Example for your terminal (replace with your actual token and desired model):
# export HF_API_KEY="hf_YOUR_NEW_REVOKED_TOKEN_HERE"
# export HF_LLAMA3_MODEL="meta-llama/Llama-3-8b-instruct" # Or "meta-llama/Llama-3-70b-instruct"

HF_API_KEY = os.getenv("HF_API_KEY")
HF_LLAMA3_MODEL = os.getenv("HF_LLAMA3_MODEL", "meta-llama/Llama-3-8B-instruct") # Default to 8B instruct

# The Hugging Face Inference API endpoint for chat completions
# This format is common for models that support the OpenAI-like chat API
LLAMA3_API_ENDPOINT = f"https://api-inference.huggingface.co/models/{HF_LLAMA3_MODEL}"

# Validating that the API key is set
if not HF_API_KEY:
    st.error("Hugging Face API Key (HF_API_KEY) not found. Please set it as an environment variable.")
    st.info("Example: `export HF_API_KEY=\"hf_YOUR_TOKEN_HERE\"` in your terminal before running `streamlit run main.py`")
    st.stop() # Stop the Streamlit app if the key is missing

# Set up page configuration
st.set_page_config(page_title="ClassGPT – AI Study Assistant", layout="centered")

# --- Internationalization (i18n) for UI Labels ---
# A basic dictionary-based approach for UI text translations.
# For more complex apps, consider dedicated Streamlit i18n libraries.
translations = {
    "English": {
        "app_title": "📚 ClassGPT – Your Smart Study Assistant",
        "tagline": "Explain topics, generate quizzes, and get summaries in English, Hausa, or Arabic!",
        "settings_header": "⚙️ Settings",
        "output_language_label": "Choose Output Language",
        "select_task_label": "Select Task",
        "explain_it": "Explain It",
        "generate_quiz": "Generate Quiz",
        "summarize_topic": "Summarize Topic",
        "try_topics_tip": "💡 Try topics like *Photosynthesis*, *The Internet*, or *Algebra*.",
        "enter_topic_prompt": "✍️ Enter a topic you’d like to study:",
        "get_response_button": "Get Response",
        "processing_message": "⏳ Processing... Please wait...",
        "success_message": "✅ Here's your result:",
        "error_api_issue": "An error occurred with the Hugging Face API. Please check your API key, model access, or network.",
        "error_parse_issue": "An unexpected response format was received from the API.",
        "error_general": "A general error occurred.",
        "start_info": "Enter a topic and click 'Get Response' to begin.",
        "quote": "> 💡 *“Education is the passport to the future, for tomorrow belongs to those who prepare for it today.”*"
    },
    "Hausa": {
        "app_title": "📚 ClassGPT – Mataimakin Nazari Mai Kaifin Hankali",
        "tagline": "Fassara batutuwa, ƙirƙira tambayoyi, da taƙaita abubuwa a Turanci, Hausa, ko Larabci!",
        "settings_header": "⚙️ Saituna",
        "output_language_label": "Zaɓi Harshen Fita",
        "select_task_label": "Zaɓi Aiki",
        "explain_it": "Fassara",
        "generate_quiz": "Ƙirƙira Tambaya",
        "summarize_topic": "Taƙaita Batu",
        "try_topics_tip": "💡 Gwada batutuwa kamar *Photosynthesis*, *Intanet*, ko *Algebra*.",
        "enter_topic_prompt": "✍️ Shigar da batu da kake son karantawa:",
        "get_response_button": "Samo Amsa",
        "processing_message": "⏳ Ana aiwatarwa... Don Allah a jira...",
        "success_message": "✅ Ga sakamakon ka:",
        "error_api_issue": "Akwai matsala da Hugging Face API. Don Allah a bincika makullin API ɗinka, damar samun samfurin, ko hanyar sadarwa.",
        "error_parse_issue": "An sami tsarin amsa da ba a tsammani daga API.",
        "error_general": "Akwai matsala gabaɗaya.",
        "start_info": "Shigar da batu sannan ka danna 'Samo Amsa' don farawa.",
        "quote": "> 💡 *“Ilimi shine fasfo zuwa gaba, domin gobe ta waɗanda suka shirya mata a yau.”*"
    },
    "Arabic": {
        "app_title": "📚 كلاس جي بي تي – مساعدك الذكي للدراسة",
        "tagline": "اشرح المواضيع، أنشئ اختبارات، واحصل على ملخصات بالإنجليزية أو الهوسا أو العربية!",
        "settings_header": "⚙️ الإعدادات",
        "output_language_label": "اختر لغة الإخراج",
        "select_task_label": "اختر المهمة",
        "explain_it": "اشرح",
        "generate_quiz": "إنشاء اختبار",
        "summarize_topic": "لخص الموضوع",
        "try_topics_tip": "💡 جرب مواضيع مثل *التمثيل الضوئي*, *الإنترنت*, أو *الجبر*.",
        "enter_topic_prompt": "✍️ أدخل موضوعًا ترغب في دراسته:",
        "get_response_button": "احصل على الرد",
        "processing_message": "⏳ جاري المعالجة... يرجى الانتظار...",
        "success_message": "✅ إليك نتيجتك:",
        "error_api_issue": "حدث خطأ في واجهة برمجة تطبيقات Hugging Face. يرجى التحقق من مفتاح API الخاص بك، أو الوصول إلى النموذج، أو الشبكة.",
        "error_parse_issue": "تم استلام تنسيق استجابة غير متوقع من واجهة برمجة التطبيقات.",
        "error_general": "حدث خطأ عام.",
        "start_info": "أدخل موضوعًا وانقر على 'احصل على الرد' للبدء.",
        "quote": "> 💡 *“التعليم هو جواز السفر إلى المستقبل، فالغد ملك لأولئك الذين يستعدون له اليوم.”*"
    }
}

# Ensure selected_language is in session state for persistence
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"

# Get the current translations based on user's selection
current_lang_texts = translations.get(st.session_state.selected_language, translations["English"])

# App Title
st.markdown(current_lang_texts["app_title"])
st.markdown(current_lang_texts["tagline"])

# Sidebar settings
with st.sidebar:
    st.markdown(current_lang_texts["settings_header"])
    
    # Language selection directly updates session state
    new_lang_selection = st.selectbox(
        current_lang_texts["output_language_label"],
        ["English", "Hausa", "Arabic"],
        index=["English", "Hausa", "Arabic"].index(st.session_state.selected_language) # Set initial value
    )
    if new_lang_selection != st.session_state.selected_language:
        st.session_state.selected_language = new_lang_selection
        st.experimental_rerun() # Rerun to apply language change immediately

    # Task selection (re-evaluate tasks based on current language)
    task_options = [
        current_lang_texts["explain_it"],
        current_lang_texts["generate_quiz"],
        current_lang_texts["summarize_topic"]
    ]
    task = st.selectbox(current_lang_texts["select_task_label"], task_options)
    st.markdown(current_lang_texts["try_topics_tip"])

# Main input section
topic = st.text_input(current_lang_texts["enter_topic_prompt"])

if st.button(current_lang_texts["get_response_button"]) and topic:
    st.markdown(current_lang_texts["processing_message"])

    # Prepare the prompt
    # Ensure LLaMA 3 is explicitly instructed to respond in the chosen language.
    prompt_map = {
        current_lang_texts["explain_it"]: f"Explain the topic '{topic}' in simple terms in {st.session_state.selected_language}. Ensure the response is clear, concise, and appropriate for an educational context.",
        current_lang_texts["generate_quiz"]: f"Create at least ten quiz questions on the topic '{topic}' in {st.session_state.selected_language}. Provide only the questions, no answer or explanation. Make it a multiple choice question with 4 options and it aligns with Nigerian educational curriculum.",
        current_lang_texts["summarize_topic"]: f"Summarize the topic '{topic}' concisely in {st.session_state.selected_language}. Focus on key information relevant to students and keep it under 150 words."
    }
    final_prompt = prompt_map[task]

    # --- Hugging Face LLaMA 3 API Request ---
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    
    # LLaMA 3 uses the 'messages' format for chat completions
    payload = {
        "model": HF_LLAMA3_MODEL,
        "messages": [
            {"role": "system", "content": f"You are a helpful, multilingual AI tutor for students. Your primary goal is to provide clear, educational content. Respond in {st.session_state.selected_language} unless explicitly asked otherwise in the user prompt."},
            {"role": "user", "content": final_prompt}
        ],
        "max_new_tokens": 700, # Increased max tokens for potentially longer explanations
        "temperature": 0.7,    # Controls creativity (0.0-1.0)
        "top_p": 0.9,          # Controls diversity (0.0-1.0)
        "do_sample": True      # Enables sampling for more varied responses
    }

    try:
        response = requests.post(LLAMA3_API_ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        llama_output = response.json()
        
        # Hugging Face Inference API for chat models usually returns an array of choices
        # The content is typically found in choices[0]['message']['content']
        output = llama_output['choices'][0]['message']['content']
        
        st.success(current_lang_texts["success_message"])
        st.write(output)
        st.code(output, language='markdown') # Useful for easy copy/paste or review of raw text

        st.markdown("---")
        st.markdown(current_lang_texts["quote"])

    except requests.exceptions.RequestException as req_err:
        st.error(f"{current_lang_texts['error_api_issue']} (Network or API connectivity problem)")
        st.text(str(req_err))
        if 'response' in locals() and response is not None:
            st.text(f"API Response Body: {response.text}") # Show API's raw response for debugging
    except (KeyError, IndexError) as parse_err:
        st.error(f"{current_lang_texts['error_parse_issue']} (Error parsing API response)")
        st.text(f"Parsing error details: {parse_err}")
        if 'llama_output' in locals():
            st.text(f"Full API Response Object: {llama_output}") # Show full object for debugging
    except Exception as e:
        st.error(f"{current_lang_texts['error_general']} (Unhandled error)")
        st.text(str(e))

else:
    st.info(current_lang_texts["start_info"])

