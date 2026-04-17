# Version 1.3 - Llama-4-Scout-17b Edition
import streamlit as st
import random
import time
from groq import Groq

# --- SETUP ---
st.set_page_config(page_title="Cosmic Bestie Tarot", page_icon="🔮", layout="centered")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: #f8f9fa; }
    div.stButton > button:first-child {
        background-color: #6A0DAD;
        color: white;
        border-radius: 12px;
        border: 1px solid #FF1493;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FF1493;
        border: 1px solid #white;
        transform: translateY(-2px);
    }
    .card-text { font-size: 1.2rem; font-weight: bold; color: #FF1493; }
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
if 'user_question' not in st.session_state:
    st.session_state.user_question = ""

# --- CLIENT ---
try:
    # Ensure your secrets.toml has the key 'GROQ_API_KEY'
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("Hold up! The cosmic key (API Key) is missing from your secrets.")
    st.stop()

# --- APP LOGIC ---

st.title("🔮 Cosmic Bestie Tarot")
st.write("---")

if st.session_state.step == "question":
    st.markdown("### ✨ What's the tea today, gorgeous?")
    q = st.text_input("Ask your question to the stars...", placeholder="Will I secure the bag this month?")
    
    if st.button("Shuffle the Vibe"):
        if q:
            st.session_state.user_question = q
            st.session_state.step = "pick"
            st.rerun()
        else:
            st.warning("Honey, I need a question to work with! Type something.")

elif st.session_state.step == "pick":
    st.markdown(f"### 🃏 Focus on: *'{st.session_state.user_question}'*")
    st.write("The deck is ready. Which one is calling your name?")
    
    # 3-Card Selection Grid
    cols = st.columns(3)
    card_options = ["Left Card", "Center Card", "Right Card"]
    
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"<div style='text-align: center;'><p class='card-text'>✨</p></div>", unsafe_allow_html=True)
            if st.button(card_options[idx]):
                st.session_state.chosen_card = random.choice(TAROT_DECK)
                st.session_state.step = "reveal"
                st.rerun()

elif st.session_state.step == "reveal":
    card = st.session_state.chosen_card
    orientation = random.choice(["Upright", "Reversed"])
    
    with st.status("Consulting Llama-4-Scout...", expanded=True) as status:
        st.write(f"You pulled: **{card} ({orientation})**")
        
        try:
            # Using the new Llama-4-Scout-17b model
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a witty, Gen-Z Cosmic Bestie tarot reader. Use modern slang (slay, tea, bestie, bet). Keep it under 100 words. Be high-energy and brutally honest but supportive."
                    },
                    {
                        "role": "user", 
                        "content": f"The question is '{st.session_state.user_question}'. The card is '{card}' in the '{orientation}' position. Give me the tea."
                    }
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                temperature=0.85,
                max_tokens=150
            )
            reading = response.choices[0].message.content
            status.update(label="Manifestation Complete!", state="complete")
        except Exception as e:
            st.error("The cosmic signal is fuzzy! (API Error)")
            reading = "The stars are literally ghosting us right now. Try again in a minute, bestie."

    # Visual Celebration
    st.balloons()
    
    # The Reveal
    with st.chat_message("assistant", avatar="✨"):
        st.write(reading)
    
    if st.button("New Reading, Who Dis?"):
        st.session_state.step = "question"
        st.rerun()
