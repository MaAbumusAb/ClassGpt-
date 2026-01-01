# ClassGPT Copilot Instructions

## Project Overview
ClassGPT is a Streamlit-based AI educational assistant that provides multilingual explanations, quizzes, and summaries using Hugging Face's LLaMA 3 model. It supports English, Hausa, and Arabic with culturally relevant content for Nigerian learners.

## Architecture
- **Single-file Streamlit app**: `class_gpt_app.py` contains the entire application
- **AI Integration**: Uses `huggingface_hub.InferenceClient` for LLaMA 3 API calls
- **Multilingual UI**: Translation dictionaries in `translations` dict with dynamic language switching
- **Session State Management**: Complex quiz flow using Streamlit session state (`st.session_state`)

## Key Patterns & Conventions

### Multilingual Support
- All UI text uses `current_lang_texts[key]` from translation dictionaries
- AI prompts explicitly instruct the model to respond in the selected language only
- Language selection triggers `st.rerun()` to update UI immediately

### Quiz System
- Quiz generation uses regex parsing (`parse_quiz_output`) to extract structured data from AI text
- Expected format: Numbered questions with A/B/C/D options, followed by "Correct Answer: [Letter]"
- Session state tracks: `quiz_data`, `quiz_answers`, `quiz_submitted`
- Quiz reset on language/level/topic changes

### Educational Levels
- Three levels: Primary (6-12), Secondary (13-18), Tertiary (18+)
- Level selection affects AI prompts for appropriate complexity
- Stored as index in `st.session_state.selected_level_index`

### API Integration
- Environment variables: `HF_TOKEN`, `HF_LLAMA3_MODEL` (defaults to meta-llama/Llama-3.1-8B-Instruct)
- Provider set to "sambanova" in InferenceClient
- Chat completions with system/user messages for prompt engineering

### Error Handling
- API failures show localized error messages
- Quiz parsing failures display raw AI output for debugging
- Environment variable validation on startup

## Development Workflow
1. Set environment variables: `HF_TOKEN` and optionally `HF_LLAMA3_MODEL`
2. Install dependencies: `pip install -r requirements.txt`
3. Run app: `streamlit run class_gpt_app.py`
4. For deployment: Use Streamlit Cloud secrets for `HF_TOKEN`

## Code Style Notes
- Use `st.session_state` for persistent UI state across reruns
- Regex patterns in `parse_quiz_output` are multiline and case-insensitive
- Translation keys match UI element purposes (e.g., `get_response_button`)
- AI prompts include educational level context for appropriate explanations

## Common Tasks
- Adding languages: Extend `translations` dict with new language keys
- Modifying quiz format: Update regex in `parse_quiz_output` and prompt template
- Adding tasks: Extend `prompt_map` dict and UI selectbox options
- UI changes: Update translation dictionaries for all supported languages