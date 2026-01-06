import streamlit as st
import json
import random

import requests

# 1. Update Configuration to 2026 Router Standard
HF_API_URL = "https://router.huggingface.co/v1/chat/completions"
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"  # High availability
HF_TOKEN = st.secrets["HF_TOKEN"]

def query_ai(prompt):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # New Payload Format
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a CS Interview Tutor. Give concise, technical answers."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            # Parsing logic for OpenAI-style response
            return result['choices'][0]['message']['content'].strip()
        else:
            return f"⚠️ Router Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"


st.set_page_config(page_title="CS Interview Bot", layout="wide", initial_sidebar_state="expanded")

# Complete Dark Theme with Blue Accents - Built from Scratch
st.markdown("""
<style>
            

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* ========== POPPINS FONT EVERYWHERE ========== */
    * {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    .stApp {
        font-family: 'Poppins', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }

   
            
    /* ========== GLOBAL DARK THEME ========== */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 50%, #0f1729 100%);
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ========== CHAT MESSAGES ========== */
    .chat-user {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 2rem 1rem 6rem;
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.4);
        font-size: 1rem;
        animation: slideRight 0.4s ease;
    }
    
    .chat-bot {
        background: rgba(25, 33, 58, 0.9);
        color: #e8eaf6;
        padding: 1.2rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 6rem 1rem 2rem;
        border-left: 4px solid #2196f3;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        font-size: 1rem;
        animation: slideLeft 0.4s ease;
    }
    
    @keyframes slideRight {
        from { opacity: 0; transform: translateX(40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* ========== QUIZ BUBBLE ========== */
    .quiz-bubble {
        background: linear-gradient(145deg, rgba(25, 33, 58, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 1rem;
        border: 2px solid #2196f3;
        box-shadow: 0 8px 30px rgba(33, 150, 243, 0.3);
        color: #e8eaf6;
    }
    
    .quiz-bubble strong {
        color: #64b5f6;
        font-weight: 700;
    }
    
    .quiz-bubble h3 {
        color: #2196f3 !important;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(33, 150, 243, 0.5);
    }
    
    /* ========== LIVE SCORE BADGE ========== */
    .score-live {
        position: fixed;
        top: 80px;
        right: 30px;
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1rem;
        z-index: 1000;
        box-shadow: 0 6px 25px rgba(33, 150, 243, 0.5);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 6px 25px rgba(33, 150, 243, 0.5); }
        50% { transform: scale(1.05); box-shadow: 0 8px 30px rgba(33, 150, 243, 0.7); }
    }
    
    /* ========== SIDEBAR STYLING ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.98) 0%, rgba(15, 23, 42, 0.98) 100%) !important;
        border-right: 2px solid rgba(33, 150, 243, 0.3);
    }
    
    [data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] h1 {
        color: #2196f3 !important;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid rgba(33, 150, 243, 0.4);
        margin-bottom: 1.5rem;
        text-shadow: 0 0 20px rgba(33, 150, 243, 0.6);
    }
    
    /* ========== SELECTBOX (DROPDOWN) ========== */
    .stSelectbox label {
        color: #64b5f6 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(25, 33, 58, 0.95) !important;
        border: 2px solid #2196f3 !important;
        border-radius: 12px !important;
        color: white !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #64b5f6 !important;
        box-shadow: 0 0 15px rgba(33, 150, 243, 0.4) !important;
    }
    
    .stSelectbox svg {
        fill: #64b5f6 !important;
    }
    
    /* Dropdown menu */
    div[role="listbox"] {
        background: rgba(15, 23, 42, 0.98) !important;
        border: 2px solid #2196f3 !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7) !important;
    }
    
    div[role="option"] {
        background: transparent !important;
        color: white !important;
        padding: 0.8rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    div[role="option"]:hover {
        background: rgba(33, 150, 243, 0.3) !important;
    }
    
    div[role="option"][aria-selected="true"] {
        background: rgba(33, 150, 243, 0.5) !important;
    }
    
    /* ========== SLIDER ========== */
    .stSlider label {
        color: #64b5f6 !important;
        font-weight: 600 !important;
    }
    
    .stSlider [data-baseweb="slider"] {
        background: transparent !important;
    }
    
    .stSlider [data-testid="stTickBar"] {
        background: rgba(33, 150, 243, 0.2) !important;
    }
    
    .stSlider [data-testid="stThumbValue"] {
        color: white !important;
        background: #2196f3 !important;
        border-radius: 8px !important;
        padding: 0.3rem 0.6rem !important;
        font-weight: 600 !important;
    }
    
    .stSlider div[role="slider"] {
        background: #2196f3 !important;
        border: 3px solid #64b5f6 !important;
        box-shadow: 0 0 10px rgba(33, 150, 243, 0.5) !important;
    }
    
    .stSlider div[role="slider"]:hover {
        box-shadow: 0 0 15px rgba(33, 150, 243, 0.8) !important;
    }
    
    .stSlider div[data-baseweb="slider"] > div > div {
        background: #2196f3 !important;
    }
    
    .stSlider div[data-baseweb="slider"] > div > div > div {
        background: rgba(33, 150, 243, 0.3) !important;
    }
    
   /* ========== TEXT INPUT (DARK + LIGHT TEXT) ========== */
.stTextInput label {
  color: #64b5f6 !important;
  font-weight: 600 !important;
}

/* BaseWeb wrapper (important in Streamlit) */
.stTextInput div[data-baseweb="base-input"] {
  background: rgba(15, 20, 35, 0.98) !important;
  background-color: rgba(15, 20, 35, 0.98) !important;
  border: 4px solid #2196f3 !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 18px rgba(33, 150, 243, 0.25) !important;
}

/* The actual input element */
.stTextInput input {
  background: transparent !important;          /* wrapper provides bg */
  color: #e8eaf6 !important;                   /* light text */
  border: none !important;                     /* wrapper provides border */
  padding: 0.85rem 1rem !important;
  font-size: 1rem !important;
  font-weight: 400 !important;
}

/* Focus state */
.stTextInput div[data-baseweb="base-input"]:focus-within {
  border-color: #64b5f6 !important;
  box-shadow: 0 0 18px rgba(100, 181, 246, 0.45) !important;
}

/* Placeholder */
.stTextInput input::placeholder {
  color: rgba(232, 234, 246, 0.55) !important;
}   

    
    /* ========== BUTTONS ========== */
    .stButton button {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(33, 150, 243, 0.4) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.6) !important;
    }
    
    .stButton button:active {
        transform: translateY(0) !important;
    }
    
  


    
    /* ========== HEADERS ========== */
    h1, h2, h3 {
        color: #2196f3 !important;
        text-shadow: 0 0 20px rgba(33, 150, 243, 0.5);
    }
    
    /* ========== GENERAL ELEMENTS ========== */
    .main .block-container {
        background: transparent !important;
        padding-bottom: 6rem !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }
    
    .stMarkdown {
        color: #e8eaf6 !important;
    }
    
    hr {
        border-color: rgba(33, 150, 243, 0.3) !important;
    }
    
    .stCaption {
        color: rgba(232, 234, 246, 0.6) !important;
        text-align: center;
    }
    
    /* Info box in sidebar */
    .stAlert {
        background: rgba(33, 150, 243, 0.15) !important;
        border: 1px solid rgba(33, 150, 243, 0.4) !important;
        border-radius: 10px !important;
        color: #e8eaf6 !important;
    }
    
    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(10, 14, 39, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64b5f6;
    }
            
    /* ========== CHAT INPUT (MODERN DARK) ========== */
.stChatFloatingInputContainer {
    background: transparent !important;
    padding: 0 !important;
}

[data-testid="stChatInputContainer"] {
    background: transparent !important;
}

[data-testid="stBottom"] {
    background: linear-gradient(180deg, transparent 0%, rgba(10, 14, 39, 0.8) 100%) !important;
    padding-top: 2rem !important;
}

[data-testid="stBottom"] > div {
    background: transparent !important;
}

/* Main input container - solid dark with glow */
[data-testid="stChatInput"] {
    background: transparent !important;  /* GitHub-dark solid */
    border: 2px solid rgba(33, 150, 243, 0.6) !important;
    border-radius: 20px !important;
    padding: 0.75rem 1.25rem !important;
    box-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.4),
        inset 0 1px 3px rgba(255, 255, 255, 0.05) !important;
    transition: all 0.3s ease !important;
}

/* Focus state - bright glow */
[data-testid="stChatInput"]:focus-within {
    border-color: #2196f3 !important;
    box-shadow: 
        0 0 0 3px rgba(33, 150, 243, 0.2),
        0 8px 30px rgba(33, 150, 243, 0.4),
        inset 0 1px 3px rgba(255, 255, 255, 0.08) !important;
    transform: translateY(-1px) !important;
}

/* Textarea styling */
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: rgba(15, 20, 35, 0.98) !important;  /* Bright white-blue */
    border: none !important;
    font-size: 1rem !important;
    font-weight: 400 !important;
    line-height: 1.5 !important;
    caret-color: #2196f3 !important;  /* Blue cursor */
}

[data-testid="stChatInput"] textarea:focus {
    outline: none !important;
}


/* Send button - icon only */
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #2196f3 0%, #1565c0 100%) !important;
    border: none !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    padding: 0 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3) !important;
}

[data-testid="stChatInput"] button:hover {
    transform: scale(1.15) rotate(5deg) !important;
    box-shadow: 0 4px 20px rgba(33, 150, 243, 0.5) !important;
    background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%) !important;
}

[data-testid="stChatInput"] button:active {
    transform: scale(0.95) !important;
}

[data-testid="stChatInput"] button svg {
    fill: white !important;
    width: 20px !important;
    height: 20px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_questions():
    with open('questions.json') as f:
        return json.load(f)

questions = load_questions()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0

# LIVE SCORE BADGE
st.markdown(f'''
<div class="score-live">
     Score: <strong>{st.session_state.quiz_score}/{st.session_state.quiz_total}</strong>
</div>
''', unsafe_allow_html=True)

# ========== SIDEBAR ==========
st.sidebar.title("Quiz Control Panel")

topic = st.sidebar.selectbox("Select Subject", list(questions.keys()))
num_q = st.sidebar.slider("Number of Questions", 3, 10, 5)

st.sidebar.markdown("---")

if st.sidebar.button("Start Quiz", use_container_width=True):
    st.session_state.quiz_questions = random.sample(questions[topic], min(num_q, len(questions[topic])))
    st.session_state.quiz_index = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_total = num_q
    st.session_state.quiz_active = True
    st.session_state.messages = []
    st.rerun()

if st.sidebar.button("Reset All", use_container_width=True):
    for key in ['quiz_questions', 'quiz_index', 'quiz_score', 'quiz_total', 'quiz_active', 'messages']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Tips")
st.sidebar.info("Select a topic, choose question count, and start your quiz!")

# ========== MAIN CHAT AREA ==========
st.title("CS Interview Prep Chatbot")
st.markdown("---")

# Display chat messages
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg['role'] == 'user':
            st.markdown(f'<div class="chat-user"> {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">👽 {msg["content"]}</div>', unsafe_allow_html=True)

# Auto-scroll to bottom
st.markdown("""
<script>
    window.addEventListener('load', function() {
        const mainContent = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        if (mainContent) {
            mainContent.scrollTop = mainContent.scrollHeight;
        }
    });
</script>
""", unsafe_allow_html=True)

# ========== QUIZ SECTION ==========
if st.session_state.get('quiz_active', False):
    q = st.session_state.quiz_questions[st.session_state.quiz_index]
    
    st.markdown(f'''
    <div class="quiz-bubble">
        <h3>Question {st.session_state.quiz_index + 1} of {len(st.session_state.quiz_questions)}</h3>
        <p style="font-size: 1.2rem; margin-bottom: 1.5rem; color: white;">
            <strong>{q['q']}</strong>
        </p>
    ''', unsafe_allow_html=True)
    
    for i, opt in enumerate(q['options']):
        st.markdown(f"<p style='font-size: 1rem; margin: 0.5rem 0; color: #e8eaf6;'><strong style='color: #64b5f6; font-weight: 700;'>{chr(97+i)})</strong> {opt}</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    ans_input = st.text_input("Your Answer (a/b/c/d)", key="quiz_ans", placeholder="Enter a, b, c, or d")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("Submit Answer", key="submit", use_container_width=True):
            user_choice = ans_input.lower().strip()
            correct_ans = q['ans']
            
            if user_choice in ['a', 'b', 'c', 'd']:
                correct_text = q['options'][ord(correct_ans) - 97]
                user_text = q['options'][ord(user_choice) - 97]
                
                if user_choice == correct_ans:
                    st.session_state.quiz_score += 1
                    feedback = f"<strong> 🟩 Correct!</strong> You chose: <strong>{user_text}</strong>"
                else:
                    feedback = f"<strong> 🟥 Incorrect!</strong> You chose: <strong>{user_text}</strong><br>✓ Correct answer: <strong>{correct_ans}) {correct_text}</strong>"
                
                st.session_state.messages.append({"role": "assistant", "content": feedback})
                
                st.session_state.quiz_index += 1
                if st.session_state.quiz_index >= st.session_state.quiz_total:
                    percentage = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
                    final_score = f"<strong>Quiz Complete!</strong><br>Final Score: <strong>{st.session_state.quiz_score}/{st.session_state.quiz_total}</strong> ({percentage:.1f}%)"
                    st.session_state.messages.append({"role": "assistant", "content": final_score})
                    st.session_state.quiz_active = False
                st.rerun()
            else:
                st.error("Please enter a valid option (a, b, c, or d)")
    
    with col2:
        if st.button("AI Explanation", key="explain", use_container_width=True):
            context = f"The user is taking a quiz on {topic}. The question is: {q['q']}. Don't give the answer yet, but explain the underlying concept to help them choose."
            with st.spinner("AI is thinking..."):
                hint = query_ai(context)
            st.session_state.messages.append({"role": "assistant", "content": f"AI Insight: {hint}"})
            st.rerun()

# ========== CHAT INPUT ==========
else:
    prompt = st.chat_input("Ask me anything about CS topics or type 'start quiz' to begin...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 1. Initialize reply with a fallback value
        reply = "" 

        with st.spinner("Thinking..."):
            # 2. Check for keywords first
            if 'quiz' in prompt.lower() and 'start' in prompt.lower():
                reply = "Great! Use the sidebar to select a topic and click 'Start Quiz' to begin your assessment."
            
            # 3. Otherwise, call the AI
            else:
                try:
                    reply = query_ai(prompt)
                except Exception as e:
                    reply = f"Sorry, I ran into an error: {str(e)}"
        
        # 4. Now 'reply' is guaranteed to exist
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
import streamlit.components.v1 as components

# --- Auto-scroll to bottom on every rerun ---
st.markdown('<div id="chat-bottom"></div>', unsafe_allow_html=True)

# Force JS to re-execute each rerun
st.session_state["scroll_i"] = st.session_state.get("scroll_i", 0) + 1

components.html(
    f"""
    <script id="scroll-script-{st.session_state['scroll_i']}">
      (function scrollToBottom() {{
        const target = window.parent.document.getElementById("chat-bottom");
        if (target) {{
          target.scrollIntoView({{ behavior: "smooth", block: "end" }});
        }} else {{
          setTimeout(scrollToBottom, 100);
        }}
      }})();
    </script>
    """,
    height=0,
)
