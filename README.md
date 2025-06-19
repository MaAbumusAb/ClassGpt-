
# ClassGPT: Your Multilingual AI Study Assistant 🌍📚



## ✨ Vision Statement

**ClassGPT** is an innovative AI-powered educational assistant dedicated to making quality learning accessible and culturally relevant for learners in Nigeria and beyond. Our core mission, as of **June 2025**, is to **bridge educational language barriers** by providing AI-driven explanations, quizzes, and summaries directly in local languages, starting with **Hausa** and **Arabic**, alongside English.

## 🌟 Features (Current MVP)

ClassGPT, in its current Minimum Viable Product (MVP) stage, showcases the power of AI to interact with users in their preferred local language:

* **Multilingual Q&A:** Engage with the AI in **English**, **Hausa**, and **Arabic**. The AI aims to understand your input and provide responses in the selected output language.
* **Three Core Tasks:**
    * **Explain It:** Get simple, clear explanations of any topic.
    * **Generate Quiz:** Create a single quiz question to test your understanding.
    * **Summarize Topic:** Obtain concise summaries of complex subjects.
* **Interactive UI:** A user-friendly interface built with Streamlit for a seamless experience.
* **Powered by LLaMA 3:** Leveraging the advanced capabilities of the LLaMA 3 model via Hugging Face Inference API for intelligent responses.

## 🚀 Getting Started

Follow these steps to get ClassGPT up and running on your local machine.

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)
* A Hugging Face account and an **API Token** with read access.

### ⚠️ Security Warning: Environment Variables

**NEVER hardcode your API tokens directly into your code.** For secure local development and deployment, we use environment variables.

1.  **Generate/Access Your Hugging Face API Token:**
    * Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
    * Generate a new token (or use an existing one). Ensure it has `read` access.
    * **Important:** If you've previously shared any token publicly, **revoke it immediately** and generate a new one.

2.  **Set Environment Variables:**
    Open your terminal or command prompt and set the following variables **before** running the app.

    * **Linux / macOS:**
        ```bash
        export HF_TOKEN="hf_YOUR_NEW_TOKEN_HERE"
        export HF_LLAMA3_MODEL="meta-llama/Llama-3-8b-instruct" # Or "meta-llama/Llama-3-70b-instruct" if you choose
        ```
    * **Windows (Command Prompt):**
        ```cmd
        set HF_TOKEN="hf_YOUR_NEW_TOKEN_HERE"
        set HF_LLAMA3_MODEL="meta-llama/Llama-3-8b-instruct"
        ```
    *Replace `"hf_YOUR_NEW_TOKEN_HERE"` with your actual Hugging Face API token.*
    *Ensure `HF_LLAMA3_MODEL` matches the exact ID of the LLaMA 3 model you intend to use on Hugging Face (and that you have accepted its license terms).*

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/MaAbumusAb/ClassGpt-](https://github.com/MaAbumusAb/ClassGpt-)
    cd ClassGpt-
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    # .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure your `requirements.txt` contains `streamlit`, `requests`, and `huggingface_hub`)*

### Running the App

Once your environment variables are set and dependencies are installed, run the Streamlit app:

```bash
streamlit run main.py
```
Your ClassGPT app should open in your web browser.
🌐 Deployment (Streamlit Cloud)
If you're deploying ClassGPT to Streamlit Cloud, here's how to securely set your API token:
 * Log in to your Streamlit Cloud dashboard.
 * Select your ClassGPT application.
 * Go to the "Settings" (three dots menu next to your app).
 * Navigate to the "Secrets" section.
 * Click "+ Add a secret".
 * For "Key", enter HF_TOKEN.
 * For "Value", paste your actual Hugging Face API token.
 * Click "Save secret".
 * Redeploy your app (or wait for automatic redeployment).
   
# 🗺️ Future Vision & Roadmap
ClassGPT is just getting started! Our ambitious roadmap includes:
 * Expanded Language Support: Integrating Pidgin and refining performance for Hausa and Arabic.
 * Curriculum Alignment: Developing structured content aligned with specific educational curricula in Nigeria.
 * Offline Access: Enabling learners to download content and continue studying without an internet connection.
 * Educator Tools: Features for teachers to generate lesson plans, track student progress, and customize learning paths.
 * Scalable Microservices Architecture: Transitioning to a modular backend for enhanced performance, reliability, and easier feature development.
 * LLaMA 3 Fine-tuning: Custom fine-tuning of LLaMA 3 models on vast datasets of local language educational content for unparalleled accuracy and fluency.
 * Mobile Applications: Developing native mobile apps for broader accessibility.
👋 Contributing
We welcome contributions! If you're passionate about leveraging AI for localized education, we'd love your help.
 * Fork the repository.
 * Create your feature branch (git checkout -b feature/AmazingFeature).
 * Commit your changes (git commit -m 'Add some AmazingFeature').
 * Push to the branch (git push origin feature/AmazingFeature).
 * Open a Pull Request.
Please ensure your code adheres to best practices and includes tests where appropriate.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📧 Contact
 * Muhammad Auwal Aliyu(Abu Mus'ab) - aliyumuhammadauwal92@gmail.com
 * Project Link: https://github.com/MaAbumusAb/ClassGpt-


