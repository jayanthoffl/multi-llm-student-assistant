import streamlit as st
import google.generativeai as genai
import openai
import os
from dotenv import load_dotenv

# Load .env and configure API keys
load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit Config
st.set_page_config(
    page_title="AI Learning Assistant",
    page_icon="🤖",
    layout="centered"
)

# Sidebar
with st.sidebar:
    st.title("AI Learning Assistant")
    st.markdown("- Google Gemini")
    st.markdown("- DeepSeek Coder")
    st.markdown("- Gemma 7B IT")
    st.caption("Note: Free model responses may take ~10–30 seconds.\nIf response not generated completely try generating again.")
    st.caption("Made by Jayanth for Timepass")

# Main Heading
st.markdown(
    "<h1 style='text-align: center;'>🎓 Student Guidance App</h1>",
    unsafe_allow_html=True
)

# Functions

def openrouter_response(prompt, model_id):
    try:
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"[OpenRouter Error] {e}"

def gemini_response(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.5,
                max_output_tokens=1000
            )
        )
        return response.text or "⚠️ No content received from Gemini."
    except Exception as e:
        return f"❌ Gemini Error: {str(e)}"

def help_with_code(code_question):
    prompt = f"Help me with this code or coding doubt:\n\n{code_question}"
    return openrouter_response(prompt, model_id="deepseek/deepseek-r1-0528:free")

def summarize_text(text):
    prompt = f"Summarize this text:\n\n{text}"
    return gemini_response(prompt)

def explain_topic(topic):
    prompt = f"Explain this topic in a detailed and easy way:\n\n{topic}"
    return gemini_response(prompt)

def create_study_plan(subject_or_goal):
    prompt = f"Make a 1-week study plan for:\n\n{subject_or_goal}"
    return openrouter_response(prompt, model_id="google/gemini-2.0-flash-exp:free")

def solve_math_problem(subject_or_goal):
    prompt = f"Solve this mathematical problem:\n\n{subject_or_goal}"
    return openrouter_response(prompt, model_id="google/gemma-3-27b-it:free")

# User Input
task = st.selectbox("Select Task:", [
    "Help with Code",
    "Summarize Text",
    "Explain Topic",
    "Create Study Plan",
    "Solve Math Problem"
])

user_input = st.text_area("Enter your text, question, or notes here:")

if st.button("Generate"):
    if user_input.strip():
        st.info(f"Working on: {task}...")

        task_map = {
            "Help with Code": help_with_code,
            "Summarize Text": summarize_text,
            "Explain Topic": explain_topic,
            "Create Study Plan": create_study_plan,
            "Solve Math Problem": solve_math_problem
        }

        result = task_map.get(task, lambda x: "Invalid Task")(user_input)
        result = result.strip() or "⚠️ No response received from the model."

        st.subheader("📘 Result")
        st.write(result)
    else:
        st.warning("Please enter something to work with.")
