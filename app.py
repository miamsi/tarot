# Version 1.4 - High Contrast & Physical Cards
import streamlit as st
import random
import time
from groq import Groq

# --- SETUP ---
st.set_page_config(page_title="Cosmic Bestie Tarot", page_icon="🔮")

# --- CUSTOM CSS (Legibility & Real Cards) ---
st.markdown("""
    <style>
    /* 1. Better Readability: Dark background but clear white/pink text */
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
        font-size: 50px;
        transition: 0.3s;
    }
    
    /* 3. High-Contrast Text for Question & Readings */
    .reading-box {
        background-color: #161122;
        border-left: 5px solid #FF1493;
        padding: 20px;
        border-radius: 10px;
        color: #FFFFFF !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* 4. Make Input Text readable */
    input { color: white !important; }
    
    h1, h2, h3 { color: #FF1493 !important; }
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
    st.error("Missing API Key in Secrets!")
    st.stop()

# --- APP ---

st.title("🔮 Cosmic Bestie Tarot")

if st.session_state.step == "question":
    st.markdown("### ✨ What's the tea today?")
    q = st.text_input("Ask your question...", placeholder="Should I text them back?")
    
    if st.button("Shuffle the Deck"):
        if q:
            st.session_state.user_question = q
            st.session_state.step = "pick"
            st.rerun()
        else:
            st.warning("I need a question to focus the energy!")

elif st.session_state.step == "pick":
    st.markdown(f"### 🃏 Question: *{st.session_state.user_question}*")
    st.write("Pick the card that 'glows' for you:")
    
    cols = st.columns(3)
    for idx, col in enumerate(cols):
        with col:
            # The "Physical" Card look
            st.markdown('<div class="tarot-card">✨</div>', unsafe_allow_html=True)
            if st.button(f"Pick Card {idx+1}", use_container_width=True):
                st.session_state.chosen_card = random.choice(TAROT_DECK)
                st.session_state.step = "reveal"
                st.rerun()

elif st.session_state.step == "reveal":
    card = st.session_state.chosen_card
    orientation = random.choice(["Upright", "Reversed"])
    
    # Reveal Animation/UI
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f'<div class="tarot-card">{card}<br><span style="font-size:15px; color:#FF1493;">({orientation})</span></div>', unsafe_allow_html=True)

    with st.spinner("Consulting Llama-4-Scout..."):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a witty, Gen-Z Cosmic Bestie reader. High contrast, high energy. Use slay, tea, bestie, bet. Max 80 words."},
                    {"role": "user", "content": f"Q: {st.session_state.user_question}. Card: {card} ({orientation})."}
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
            reading = response.choices[0].message.content
        except Exception:
            reading = "The stars are ghosting us. Try again!"

    st.markdown(f'<div class="reading-box">{reading}</div>', unsafe_allow_html=True)
    
    if st.button("Ask Again"):
        st.session_state.step = "question"
        st.rerun()
