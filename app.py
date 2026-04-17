# Version 1.7 - Error Proof 3-Card Spread
import streamlit as st
import random
from groq import Groq

# --- SETUP ---
st.set_page_config(page_title="Cosmic Bestie Tarot", page_icon="🔮")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0A0414; color: #FFFFFF; }
    .tarot-card {
        background: linear-gradient(135deg, #1e1233 0%, #3a2359 100%);
        border: 2px solid #FF1493;
        border-radius: 12px;
        padding: 20px 10px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
        color: #FFFFFF;
        font-weight: bold;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .card-label { color: #FF1493; font-size: 0.8rem; margin-top: 5px; text-transform: uppercase; }
    div.stButton > button {
        background-color: #6A0DAD !important;
        color: #FFFFFF !important;
        border: 2px solid #FF1493 !important;
        border-radius: 10px !important;
    }
    div.stButton > button:hover { background-color: #FF1493 !important; }
    .reading-box {
        background-color: #161122;
        border-left: 5px solid #FF1493;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ---
TAROT_DECK = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "The World"]

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state.step = "question"
if 'picks' not in st.session_state: st.session_state.picks = []
if 'user_question' not in st.session_state: st.session_state.user_question = ""

# --- CLIENT ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("API Key missing!")
    st.stop()

# --- APP FLOW ---
st.title("🔮 Cosmic Bestie Tarot")

if st.session_state.step == "question":
    q = st.text_input("Ask about your past, present, and future...", placeholder="Will my life finally make sense?")
    if st.button("Consult the Stars"):
        if q:
            st.session_state.user_question = q
            st.session_state.picks = [] # Clear old picks
            st.session_state.step = "pick"
            st.rerun()

elif st.session_state.step == "pick":
    st.subheader(f"Pick 3 cards for your spread...")
    progress = len(st.session_state.picks)
    st.write(f"Cards selected: {progress} / 3")
    
    # Simple grid for picking
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            st.markdown('<div class="tarot-card">✨</div>', unsafe_allow_html=True)
            # Use unique keys to avoid button conflicts
            if st.button(f"Draw Card {i+1}", key=f"pick_btn_{i}_{progress}"):
                if len(st.session_state.picks) < 3:
                    card = random.choice(TAROT_DECK)
                    orient = random.choice(["Upright", "Reversed"])
                    st.session_state.picks.append({"name": card, "pos": orient})
                
                if len(st.session_state.picks) == 3:
                    st.session_state.step = "reveal"
                st.rerun()

elif st.session_state.step == "reveal":
    # SAFETY CHECK: If we got here by accident without 3 cards, go back
    if len(st.session_state.picks) < 3:
        st.session_state.step = "pick"
        st.rerun()
        
    st.markdown(f"### ✨ The Universe's Response")
    p = st.session_state.picks
    
    # Display the 3-Card Spread
    cols = st.columns(3)
    labels = ["PAST", "PRESENT", "FUTURE"]
    for i in range(3):
        with cols[i]:
            # This is the line that was crashing; now p[i] is guaranteed to exist
            st.markdown(f'''
                <div class="tarot-card">
                    {p[i]["name"]}
                    <br><span class="card-label">{p[i]["pos"]}</span>
                    <br><span style="font-size:10px; opacity:0.6;">{labels[i]}</span>
                </div>
                ''', unsafe_allow_html=True)

    with st.spinner("Llama-4-Scout is weaving your story..."):
        try:
            prompt = f"Question: {st.session_state.user_question}. Spread: 1. Past: {p[0]['name']} ({p[0]['pos']}), 2. Present: {p[1]['name']} ({p[1]['pos']}), 3. Future: {p[2]['name']} ({p[2]['pos']})."
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a witty Gen-Z Tarot Bestie. Interpret this 3-card spread as one story. Use slang. Max 100 words."},
                    {"role": "user", "content": prompt}
                ],
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
            reading = response.choices[0].message.content
        except:
            reading = "The cosmic WiFi is down, bestie. Try again!"

    st.markdown(f'<div class="reading-box">{reading}</div>', unsafe_allow_html=True)
    
    if st.button("New Reading"):
        st.session_state.step = "question"
        st.session_state.picks = []
        st.rerun()
