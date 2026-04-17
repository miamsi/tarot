# Version 1.5 - Fixed Contrast & Interactive Cards
import streamlit as st
import random
from groq import Groq

# --- SETUP ---
st.set_page_config(page_title="Cosmic Bestie Tarot", page_icon="🔮")

# --- CUSTOM CSS (Legibility & Button Fixes) ---
st.markdown("""
    <style>
    /* 1. Global Page Style */
    .stApp { 
        background-color: #0A0414; 
        color: #FFFFFF; 
    }
    
    /* 2. Style for "Real" Cards */
    .tarot-card {
        background: linear-gradient(135deg, #1e1233 0%, #3a2359 100%);
        border: 2px solid #FF1493;
        border-radius: 15px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        margin-bottom: 10px;
        font-size: 40px;
        font-weight: bold;
        color: #FFFFFF;
    }
    
    /* 3. Button Customization (The Fix) */
    div.stButton > button {
        background-color: #6A0DAD !important;
        color: #FFFFFF !important;
        border: 2px solid #FF1493 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #FF1493 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
    }
    
    /* 4. Reading Box Style */
    .reading-box {
        background-color: #161122;
        border: 1px solid #3A2359;
        border-left: 5px solid #FF1493;
        padding: 20px;
        border-radius: 10px;
        color: #FFFFFF !important;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-top: 20px;
    }

    /* 5. Ensuring Input Labels and Text are Visible */
    label, .stMarkdown, p {
        color: #E2D4F0 !important;
    }
    
    input {
        background-color: #1E1233 !important;
        color: white !important;
        border: 1px solid #FF1493 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DECK DATA ---
TAROT_DECK = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "The World"
]

# --- SESSION STATE ---
if 'step' not in st.session_state:
    st.session_state.step = "question"

# --- CLIENT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Missing API Key! Check your Secrets dashboard.")
    st.stop()

# --- APP FLOW ---

st.title("🔮 Cosmic Bestie Tarot")

if st.session_state.step == "question":
    st.markdown("### ✨ What's the vibe today?")
    q = st.text_input("Ask your question...", placeholder="Should I quit my job and become a DJ?")
    
    if st.button("Shuffle & Connect"):
        if q:
            st.session_state.user_question = q
            st.session_state.step = "pick"
            st.rerun()
        else:
            st.warning("Bestie, I need a question first!")

elif st.session_state.step == "pick":
    st.markdown(f"### 🃏 Focus on: *{st.session_state.user_question}*")
    st.write("The spirits have shuffled. Choose your destiny:")
    
    cols = st.columns(3)
    card_labels = ["Left Path", "Inner Voice", "Right Path"]
    
    for idx, col in enumerate(cols):
        with col:
            st.markdown('<div class="tarot-card">✨</div>', unsafe_allow_html=True)
            if st.button(card_labels[idx]):
                st.session_state.chosen_card = random.choice(TAROT_DECK)
                st.session_state.step = "reveal"
                st.rerun()

elif st.session_state.step == "reveal":
    card = st.session_state.chosen_card
    orientation = random.choice(["Upright", "Reversed"])
    
    # Visual Reveal
    st.markdown(f'<div class="tarot-card">{card}<br><span style="font-size:16px; color:#FF1493;">{orientation}</span></div>', unsafe_allow_html=True)

    with st.spinner("Llama-4-Scout is checking the stars..."):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a witty, Gen-Z Cosmic Bestie reader. Use slang like slay, tea, bestie, bet. Max 80 words."},
                    {"role": "user", "content": f"Q: {st.session_state.user_question}. Card: {card} ({orientation})."}
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
            reading = response.choices[0].message.content
        except Exception:
            reading = "The connection to the astral plane is weak! Try again, babe."

    st.markdown(f'<div class="reading-box">{reading}</div>', unsafe_allow_html=True)
    
    if st.button("Another Question?"):
        st.session_state.step = "question"
        st.rerun()
