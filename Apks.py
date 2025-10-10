import streamlit as st
import google.generativeai as genai
import toml

# ======================================
# 🌟 LOAD API KEY FROM config.toml
# ======================================
try:
    config = toml.load("config.toml")
    API_KEY = config['gemini']['api_key']
except Exception as e:
    st.error(f"⚠️ Could not load API key: {e}")
    API_KEY = None

# ======================================
# 🌟 INITIALIZE GEMINI 2.5 FLASH
# ======================================
model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        st.success("✅ Gemini initialized successfully!")
    except Exception as e:
        st.error(f"⚠️ Gemini initialization failed: {e}")
else:
    st.error("⚠️ API key missing!")

# ======================================
# 🌈 STREAMLIT PAGE CONFIG
# ======================================
st.set_page_config(page_title="AI Study Buddy 🤖", layout="wide")

# Custom background & styles
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #c9e4de, #eef6f9, #e4e0f1);
    animation: gradientShift 15s ease infinite;
    background-size: 400% 400%;
}
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
h1,h2,h3,h4 { color:#004d61; }
.stButton>button {
    background-color:#00acc1;color:white;font-weight:bold;border-radius:10px;
    padding:10px 20px;transition:0.3s;
}
.stButton>button:hover {background-color:#007c91;}
</style>
""", unsafe_allow_html=True)

# ======================================
# GEMINI RESPONSE FUNCTION
# ======================================
def ask_gemini(prompt):
    if not model:
        return "⚠️ Gemini model not initialized."
    try:
        # Ensure short, readable response
        prompt = f"{prompt}\nRespond briefly and concisely."
        response = model.generate_content([prompt])
        
        # ✅ Extract readable text
        if hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content  # <- human-readable
        else:
            return "⚠️ No response from Gemini."
    except Exception as e:
        return f"⚠️ Error while calling Gemini: {e}"

# ======================================
# SIDEBAR MENU
# ======================================
st.sidebar.title("📚 Study Buddy Menu")
menu = st.sidebar.radio("Navigate:", [
    "🏠 Home","🧠 Explain Topic","📝 Summarize Notes",
    "🎯 Generate Quiz","💡 Flashcards","❓ Ask Question","ℹ️ About"
])

# ======================================
# HOME PAGE
# ======================================
if menu == "🏠 Home":
    st.title("Welcome to AI Study Buddy 🤖")
    st.markdown("""
👋 **Hi Student!**  
I'm your **AI-powered Study Buddy**, ready to make your learning journey smoother.  
I can help you with:
- 🧠 Explaining tough topics  
- 📝 Summarizing long notes  
- 🎯 Generating quizzes  
- 💡 Creating flashcards  
- ❓ Answering study questions  
""")
    st.info("👉 Select a tool from the left sidebar to get started!")

# ======================================
# EXPLAIN TOPIC
# ======================================
elif menu == "🧠 Explain Topic":
    st.header("🧠 Topic Explanation")
    topic = st.text_input("Enter your topic:")
    if st.button("Explain ✨"):
        if topic.strip():
            with st.spinner("Thinking... 🧩"):
                result = ask_gemini(f"Explain the topic '{topic}' in easy language for students.")
                st.success("Here’s your explanation 💡")
                st.write(result)
        else:
            st.warning("Please enter a topic!")

# ======================================
# SUMMARIZE NOTES
# ======================================
elif menu == "📝 Summarize Notes":
    st.header("📝 Summarize Your Notes")
    notes = st.text_area("Paste your study notes here:")
    if st.button("Summarize 🧠"):
        if notes.strip():
            with st.spinner("Summarizing... 🪄"):
                result = ask_gemini(f"Summarize these notes into short key points:\n{notes}")
                st.success("Summary Ready ✅")
                st.write(result)
        else:
            st.warning("Please paste your notes!")

# ======================================
# GENERATE QUIZ
# ======================================
elif menu == "🎯 Generate Quiz":
    st.header("🎯 Quiz Generator")
    quiz_topic = st.text_input("Enter quiz topic:")
    if st.button("Generate Quiz 📋"):
        if quiz_topic.strip():
            with st.spinner("Creating quiz questions... ✍️"):
                result = ask_gemini(f"Create 5 multiple choice questions with options and correct answers about '{quiz_topic}'.")
                st.success("Quiz Generated 🎉")
                st.write(result)
        else:
            st.warning("Please enter a topic!")

# ======================================
# FLASHCARDS
# ======================================
elif menu == "💡 Flashcards":
    st.header("💡 Flashcard Creator")
    flash_topic = st.text_input("Enter topic for flashcards:")
    if st.button("Generate Flashcards 🪄"):
        if flash_topic.strip():
            with st.spinner("Generating flashcards... 🎴"):
                result = ask_gemini(f"Generate 5 flashcards for '{flash_topic}' in term:definition format.")
                st.success("Flashcards Ready! 🃏")
                st.write(result)
        else:
            st.warning("Please enter a topic!")

# ======================================
# ASK QUESTION
# ======================================
elif menu == "❓ Ask Question":
    st.header("❓ Ask AI Anything (Study Mode)")
    question = st.text_input("Type your question:")
    if st.button("Get Answer 💬"):
        if question.strip():
            with st.spinner("Finding answer... 🔍"):
                result = ask_gemini(f"Answer this question clearly and simply:\n{question}")
                st.success("Answer Ready! 🧠")
                st.write(result)
        else:
            st.warning("Please type a question!")

# ======================================
# ABOUT PAGE
# ======================================
elif menu == "ℹ️ About":
    st.header("ℹ️ About AI Study Buddy")
    st.write("""
💡 **AI Study Buddy** is an interactive AI assistant for students.  
It helps with:
- Explaining topics  
- Summarizing notes  
- Creating quizzes  
- Making flashcards  
- Answering study questions  
---
🧑‍💻 Developed by Darshil’s AI Team  
Powered by **Gemini 2.5 Flash** 🚀
""")
