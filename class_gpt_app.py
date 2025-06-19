import streamlit as st
import os
from huggingface_hub import InferenceClient
import json
import re # For parsing quiz output

# --- Configuration for Hugging Face LLaMA 3 Inference API ---
HF_API_KEY = os.getenv("HF_TOKEN")
HF_LLAMA3_MODEL = os.getenv("HF_LLAMA3_MODEL", "meta-llama/Llama-3-8b-instruct")

# The Hugging Face Inference API endpoint for chat completions
LLAMA3_API_ENDPOINT = f"https://api-inference.huggingface.co/models/{HF_LLAMA3_MODEL}"

# Validate that the API key is set
if not HF_API_KEY:
    st.error("Hugging Face API Key (HF_TOKEN) not found. Please set it as an environment variable.")
    st.info("Example: `export HF_TOKEN=\"hf_YOUR_TOKEN_HERE\"` in your terminal before running `streamlit run main.py`")
    st.stop() # Stop the Streamlit app if the key is missing

try:
    hf_client = InferenceClient(
        provider="sambanova", # Confirm this provider is correct for your model access
        api_key=HF_API_KEY,
    )
except Exception as e:
    st.error(f"Failed to initialize Hugging Face Inference Client. Please check your HF_TOKEN and provider settings: {e}")
    st.stop()

st.set_page_config(page_title="ClassGPT – AI Study Assistant", layout="centered")

# --- Internationalization (i18n) for UI Labels ---
translations = {
    "English": {
        "app_title": "📚 ClassGPT – Your Smart Study Assistant",
        "tagline": "Explain topics, generate quizzes, and get summaries in English, Hausa, or Arabic!",
        "settings_header": "⚙️ Settings",
        "output_language_label": "Choose Output Language",
        "select_task_label": "Select Task",
        "level_label": "Choose Your Educational Level", # NEW
        "level_primary": "Primary School (Ages 6-12)", # NEW
        "level_secondary": "Secondary School (Ages 13-18)", # NEW
        "level_tertiary": "Tertiary/University (Ages 18+)", # NEW
        "explain_it": "Explain It",
        "generate_quiz": "Generate Quiz",
        "summarize_topic": "Summarize Topic",
        "try_topics_tip": "💡 Try topics like *Photosynthesis*, *The Internet*, or *Algebra*.",
        "enter_topic_prompt": "✍️ Enter a topic you’d like to study:",
        "num_questions_label": "Number of Quiz Questions",
        "get_response_button": "Get Response",
        "submit_quiz_button": "Submit Quiz",
        "processing_message": "⏳ Processing... Please wait...",
        "success_message": "✅ Here's your result:",
        "quiz_score": "📊 Your Quiz Score:",
        "quiz_correct_answer": "Correct Answer:",
        "your_answer": "Your Answer:",
        "error_api_issue": "An error occurred with the Hugging Face API. Please check your API token, model access, or network.",
        "error_parse_issue": "An unexpected response format was received from the API. Quiz parsing failed.",
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
        "level_label": "Zaɓi Matakin Karatunka", # NEW
        "level_primary": "Makarantar Firamare (Shekaru 6-12)", # NEW
        "level_secondary": "Makarantar Sakandare (Shekaru 13-18)", # NEW
        "level_tertiary": "Jami'a/Manyan Makarantu (Shekaru 18+)", # NEW
        "explain_it": "Fassara",
        "generate_quiz": "Ƙirƙira Tambaya",
        "summarize_topic": "Taƙaita Batu",
        "try_topics_tip": "💡 Gwada batutuwa kamar *Photosynthesis*, *Intanet*, ko *Algebra*.",
        "enter_topic_prompt": "✍️ Shigar da batu da kake son karantawa:",
        "num_questions_label": "Adadin Tambayoyin Jarrabawa",
        "get_response_button": "Samo Amsa",
        "submit_quiz_button": "Aika Amsoshin Jarrabawa",
        "processing_message": "⏳ Ana aiwatarwa... Don Allah a jira...",
        "success_message": "✅ Ga sakamakon ka:",
        "quiz_score": "📊 Sakamakon Jarrabawar ka:",
        "quiz_correct_answer": "Amsa Daidai:",
        "your_answer": "Amsar ka:",
        "error_api_issue": "Akwai matsala da Hugging Face API. Don Allah a bincika makullin API ɗinka, damar samun samfurin, ko hanyar sadarwa.",
        "error_parse_issue": "An sami tsarin amsa da ba a tsammani daga API. Tsarin jarrabawa ya gagara.",
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
        "level_label": "اختر مستواك التعليمي", # NEW
        "level_primary": "المرحلة الابتدائية (6-12 سنة)", # NEW
        "level_secondary": "المرحلة الثانوية (13-18 سنة)", # NEW
        "level_tertiary": "التعليم العالي/الجامعة (18+ سنة)", # NEW
        "explain_it": "اشرح",
        "generate_quiz": "إنشاء اختبار",
        "summarize_topic": "لخص الموضوع",
        "try_topics_tip": "💡 جرب مواضيع مثل *التمثيل الضوئي*, *الإنترنت*, أو *الجبر*.",
        "enter_topic_prompt": "✍️ أدخل موضوعًا ترغب في دراسته:",
        "num_questions_label": "عدد أسئلة الاختبار",
        "get_response_button": "احصل على الرد",
        "submit_quiz_button": "إرسال الاختبار",
        "processing_message": "⏳ جاري المعالجة... يرجى الانتظار...",
        "success_message": "✅ إليك نتيجتك:",
        "quiz_score": "📊 نتيجتك في الاختبار:",
        "quiz_correct_answer": "الإجابة الصحيحة:",
        "your_answer": "إجابتك:",
        "error_api_issue": "حدث خطأ في واجهة برمجة تطبيقات Hugging Face. يرجى التحقق من مفتاح API الخاص بك، أو الوصول إلى النموذج، أو الشبكة.",
        "error_parse_issue": "تم استلام تنسيق استجابة غير متوقع من واجهة برمجة التطبيقات. فشل تحليل الاختبار.",
        "error_general": "حدث خطأ عام.",
        "start_info": "أدخل موضوعًا وانقر على 'احصل على الرد' للبدء.",
        "quote": "> 💡 *“التعليم هو جواز السفر إلى المستقبل، فالغد ملك لأولئك الذين يستعدون له اليوم.”*"
    }
}

# Ensure session states are initialized
if "selected_language" not in st.session_state:
    st.session_state.selected_language = "English"
if "selected_level" not in st.session_state: # NEW: Initialize selected_level
    st.session_state.selected_level = translations["English"]["level_secondary"] # Default to Secondary
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


# Get the current translations based on user's selection
current_lang_texts = translations.get(st.session_state.selected_language, translations["English"])

# App Title
st.markdown(current_lang_texts["app_title"])
st.markdown(current_lang_texts["tagline"])

# Sidebar settings
with st.sidebar:
    st.markdown(current_lang_texts["settings_header"])
    
    # Language selection
    new_lang_selection = st.selectbox(
        current_lang_texts["output_language_label"],
        ["English", "Hausa", "Arabic"],
        index=["English", "Hausa", "Arabic"].index(st.session_state.selected_language)
    )
    if new_lang_selection != st.session_state.selected_language:
        st.session_state.selected_language = new_lang_selection
        st.session_state.quiz_data = None # Clear quiz if language changes
        st.session_state.quiz_submitted = False
        st.experimental_rerun()

    # Level selection - uses the NEW translation keys
    educational_levels = [
        current_lang_texts["level_primary"],
        current_lang_texts["level_secondary"],
        current_lang_texts["level_tertiary"]
    ]
    new_level_selection = st.selectbox(
        current_lang_texts["level_label"],
        options=educational_levels,
        index=educational_levels.index(st.session_state.selected_level) # Maintain previous selection
    )
    if new_level_selection != st.session_state.selected_level:
        st.session_state.selected_level = new_level_selection
        st.session_state.quiz_data = None # Clear quiz if level changes
        st.session_state.quiz_submitted = False
        st.experimental_rerun()

    task = st.selectbox(current_lang_texts["select_task_label"],
                        [current_lang_texts["explain_it"], current_lang_texts["generate_quiz"], current_lang_texts["summarize_topic"]])
    st.markdown(current_lang_texts["try_topics_tip"])

    num_questions = 1 # Default
    if task == current_lang_texts["generate_quiz"]: # Only show for quiz task
        num_questions = st.number_input(
            current_lang_texts["num_questions_label"],
            min_value=1,
            max_value=5, # Limit for performance/cost
            value=1,
            step=1
        )
        if st.session_state.get('last_num_questions') != num_questions:
             st.session_state.quiz_data = None # Clear quiz if number of questions changes
             st.session_state.quiz_submitted = False
             st.session_state.last_num_questions = num_questions


# Main input section
topic = st.text_input(current_lang_texts["enter_topic_prompt"])

# --- Helper function to parse quiz output ---
def parse_quiz_output(raw_text, lang_texts):
    questions = []
    # This regex attempts to find numbered questions, options (A-D), and the correct answer.
    # It's robust but may need tweaking based on actual LLM output patterns.
    # It looks for:
    # 1. Start of a line with a number and a dot (e.g., "1. Question text")
    # 2. Captures the question text.
    # 3. Captures options labeled A), B), C), D) and their text.
    # 4. Captures the "Correct Answer: [Letter]" line.
    pattern = re.compile(
        r'^\s*(\d+)\.\s*(.*?)\n' # Question number and text
        r'(?:\s*([A-D])\)\s*(.*?)\n){4}' # Four options A-D
        r'(?:Correct Answer|' + re.escape(lang_texts["quiz_correct_answer"]) + r'):\s*([A-D])', # Correct Answer line
        re.MULTILINE | re.DOTALL | re.IGNORECASE
    )

    for match in pattern.finditer(raw_text):
        q_num = int(match.group(1))
        question_text = match.group(2).strip()
        
        options = {
            match.group(3).upper(): match.group(4).strip(), # A)
            match.group(5).upper(): match.group(6).strip(), # B)
            match.group(7).upper(): match.group(8).strip(), # C)
            match.group(9).upper(): match.group(10).strip() # D)
        }
        correct_answer = match.group(11).upper().strip()

        if question_text and options and correct_answer:
            questions.append({
                "question": question_text,
                "options": options,
                "correct_answer": correct_answer
            })
    return questions


# --- Main App Logic ---
if st.button(current_lang_texts["get_response_button"]) and topic:
    st.markdown(current_lang_texts["processing_message"])
    st.session_state.quiz_data = None # Clear previous quiz
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False

    # Retrieve the selected educational level
    selected_education_level = st.session_state.selected_level

    # Prepare the prompt
    # System prompt is now dependent on selected_education_level
    system_prompt_template = f"""You are ClassGPT, an expert educational tutor and assistant.
Your primary goal is to provide clear, concise, and accurate educational content for students.
You are fluent in English, Hausa, and Arabic.
Strictly adhere to the requested output language. **Do NOT include any English words or phrases in your output unless they are proper nouns (e.g., 'Google', 'Nigeria') or universally accepted scientific terms without a common translation.**
Explain concepts in simple terms suitable for learners at a {selected_education_level} level.
"""
    prompt_map = {
        current_lang_texts["explain_it"]: f"""Explain the topic '{topic}' in simple and easy-to-understand terms.
Ensure the explanation is appropriate for a {selected_education_level} student level.
Use clear and concise sentences.
Provide concrete examples relevant to everyday life in Nigeria if applicable.
The entire explanation MUST be in {st.session_state.selected_language}.
""",
        current_lang_texts["generate_quiz"]: f"""Generate exactly {num_questions} multiple-choice questions about the topic '{topic}'.
Ensure questions are appropriate for a {selected_education_level} student level.
Each question and all its options MUST be in {st.session_state.selected_language}.
For each question, provide 4 options, labeled A, B, C, D.
After the options for each question, explicitly state the correct answer on a new line in the format: "Correct Answer: [Option Letter]".
DO NOT provide explanations for the answers or any additional text apart from the questions, options, and correct answers.

Example Format for a single question:
1. What is the capital of France?
A) Berlin
B) Paris
C) Rome
D) Madrid
Correct Answer: B

2. What is the largest planet in our solar system?
A) Mars
B) Earth
C) Jupiter
D) Venus
Correct Answer: C
""",
        current_lang_texts["summarize_topic"]: f"""Provide a concise summary of the topic '{topic}'.
Focus only on the most critical information relevant to a {selected_education_level} student.
The summary MUST be in {st.session_state.selected_language}.
Keep the summary to a maximum of 150 words or 3 paragraphs, whichever is shorter.
"""
    }
    final_prompt = prompt_map[task]

    # --- Hugging Face LLaMA 3 API Request using InferenceClient ---
    try:
        completion = hf_client.chat.completions.create(
            model=HF_LLAMA3_MODEL,
            messages=[
                {"role": "system", "content": system_prompt_template},
                {"role": "user", "content": final_prompt}
            ],
            max_tokens=1500 if task == current_lang_texts["generate_quiz"] else 700, # More tokens for multiple questions
            temperature=0.7,
            top_p=0.9,
            # do_sample=True # Removed as per previous TypeError
        )
        
        output = completion.choices[0].message.content
        
        if task == current_lang_texts["generate_quiz"]:
            parsed_quiz = parse_quiz_output(output, current_lang_texts)
            if parsed_quiz:
                st.session_state.quiz_data = parsed_quiz
                st.session_state.quiz_answers = {f"q{i}": None for i in range(len(parsed_quiz))}
                st.session_state.quiz_submitted = False
                st.success(current_lang_texts["success_message"])
                st.write("Quiz Generated! Please answer the questions below.")
            else:
                st.error(f"{current_lang_texts['error_parse_issue']} The AI did not generate a parsable quiz. Please try again or refine the topic.")
                st.code(output, language='markdown') # Show raw output for debugging
        else:
            st.success(current_lang_texts["success_message"])
            st.write(output)
            st.code(output, language='markdown') 

        st.markdown("---")
        st.markdown(current_lang_texts["quote"])

    except Exception as e:
        st.error(f"{current_lang_texts['error_api_issue']} (Details: {e})")
        st.text(f"Error type: {type(e).__name__}")
        st.text(f"Error message: {str(e)}")

else:
    st.info(current_lang_texts["start_info"])


# --- Display Quiz and Collect Answers ---
if st.session_state.quiz_data and not st.session_state.quiz_submitted:
    st.markdown("### Take the Quiz!")
    with st.form("quiz_form"):
        user_answers = {}
        for i, q_data in enumerate(st.session_state.quiz_data):
            st.markdown(f"**{i+1}. {q_data['question']}**")
            options_list = [f"{k}) {q_data['options'][k]}" for k in sorted(q_data['options'].keys())]
            user_answers[f"q{i}"] = st.radio(
                f"Select your answer for question {i+1}",
                options=options_list,
                key=f"q_{i}_radio" # Unique key for Streamlit widgets
            )
        
        if st.form_submit_button(current_lang_texts["submit_quiz_button"]):
            # Extract just the option letter (A, B, C, D) from the user's selection
            st.session_state.quiz_answers = {k: v.split(')')[0] if v else None for k, v in user_answers.items()}
            st.session_state.quiz_submitted = True
            st.experimental_rerun() # Rerun to show results

# --- Display Quiz Results ---
if st.session_state.quiz_data and st.session_state.quiz_submitted:
    st.markdown(f"## {current_lang_texts['quiz_score']}")
    score = 0
    total_questions = len(st.session_state.quiz_data)

    for i, q_data in enumerate(st.session_state.quiz_data):
        st.markdown(f"**{i+1}. {q_data['question']}**")
        
        user_choice_letter = st.session_state.quiz_answers.get(f"q{i}")
        correct_answer_letter = q_data['correct_answer']
        
        user_choice_text = q_data['options'].get(user_choice_letter, "No Answer Selected") # Handle case where user didn't select
        correct_answer_text = q_data['options'].get(correct_answer_letter, "N/A")

        if user_choice_letter == correct_answer_letter:
            score += 1
            st.success(f"Correct! 🎉 {current_lang_texts['your_answer']} {user_choice_letter}) {user_choice_text}")
        else:
            st.error(f"Incorrect. ❌ {current_lang_texts['your_answer']} {user_choice_letter}) {user_choice_text}")
            st.info(f"{current_lang_texts['quiz_correct_answer']} {correct_answer_letter}) {correct_answer_text}")
        st.markdown("---")
    
    st.markdown(f"## {current_lang_texts['quiz_score']} {score}/{total_questions}")
    if score == total_questions:
        st.balloons()
        st.markdown("### Congratulations! You got all the answers correct! 🥳")
    elif score >= total_questions * 0.7:
        st.markdown("### Good job! Keep up the great work! 👍")
    else:
        st.markdown("### You can do better! Keep studying! 💪")

    if st.button("Generate a New Quiz"):
        st.session_state.quiz_data = None
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.experimental_rerun()

