# Version 1
import streamlit as st
import random
import time
from groq import Groq

# --- CONFIGURATION & SETUP ---
st.set_page_config(page_title="Cosmic Bestie Tarot", page_icon="✨", layout="centered")

# --- CUSTOM CSS FOR FUN UX ---
st.markdown("""
    <style>
    /* Main background and text */
    .stApp {
        background-color: #120A21;
        color: #E2D4F0;
    }
    
    /* Style the main button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #6A0DAD 0%, #FF1493 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px;
        font-size: 20px;
        font-weight: bold;
        transition: transform 0.2s ease-in-out;
    }
    
    /* Button hover effect */
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px rgba(255, 20, 147, 0.6);
        color: white;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: #1E1233 !important;
        border-radius: 15px;
        border: 1px solid #3A2359;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TAROT DATA ---
TAROT_DECK = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World", "Ace of Wands", "Two of Swords", "Ten of Cups", "King of Pentacles"
    # Keeping the list concise for the code block, but you can add all 78 here!
]

# --- SESSION STATE ---
# We use session state so the reading doesn't disappear if the user clicks somewhere else
if 'reading_history' not in st.session_state:
    st.session_state.reading_history = []

# --- GROQ CLIENT INITIALIZATION ---
# Good Error Handling: Check if API key exists before trying to initialize
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except KeyError:
    st.error("🚨 Missing API Key! Please set GROQ_API_KEY in your .streamlit/secrets.toml file.")
    st.stop()

# --- UI HEADER ---
st.title("✨ Cosmic Bestie Tarot")
st.subheader("Spilling the universe's tea, just for you.")

# --- USER INPUT ---
user_question = st.text_input("What's on your mind, gorgeous?", placeholder="e.g., Will I survive this week?")

# --- MAIN LOGIC ---
if st.button("🔮 Reveal My Fate"):
    if not user_question.strip():
        st.warning("Oops! You gotta ask a question first so the universe knows what to answer.")
    else:
        # Fun UX: Visual loading states
        with st.spinner("Shuffling the cosmic deck..."):
            time.sleep(1) # Artificial delay for suspense
            
            # Draw a card
            drawn_card = random.choice(TAROT_DECK)
            is_reversed = random.choice([True, False])
            orientation = "Reversed" if is_reversed else "Upright"
            
        with st.spinner("Channeling the energy..."):
            # SYSTEM PROMPT: Token efficient but high personality
            system_prompt = """
            You are a fun, Gen-Z 'Cosmic Bestie' tarot reader. 
            Keep your response under 150 words to be quick and punchy. 
            Use 2-3 emojis. Be supportive but witty. Do not explain the card's traditional meaning boringly; apply it directly to the user's question with your persona.
            """
            
            user_prompt = f"My question is: '{user_question}'. I drew the {drawn_card} ({orientation}). What's the tea?"
            
            try:
                # Groq API Call
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="meta-llama/llama-4-scout-17b-16e-instruct", # Fast and token-efficient model
                    temperature=0.8, # Slightly high for creativity
                    max_tokens=250 # Hard limit to prevent token bleeding
                )
                
                ai_response = chat_completion.choices[0].message.content
                
                # Save to history
                st.session_state.reading_history.insert(0, {
                    "question": user_question,
                    "card": f"{drawn_card} ({orientation})",
                    "response": ai_response
                })
                
                st.balloons() # Fun UX trigger on success
                
            except Exception as e:
                # Good Error Handling for API failures (Rate limits, connection drops)
                st.error("🚨 The universe is experiencing technical difficulties! (Groq API Error)")
                st.code(str(e))

# --- DISPLAY HISTORY ---
# Shows the most recent reading at the top
if st.session_state.reading_history:
    st.divider()
    st.subheader("Your Readings 📖")
    
    for reading in st.session_state.reading_history:
        with st.container():
            st.markdown(f"**You asked:** {reading['question']}")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                # Placeholder for actual card images later
                st.info(f"🃏 {reading['card']}")
            with col2:
                with st.chat_message("assistant"):
                    st.write(reading['response'])
        st.markdown("---")
