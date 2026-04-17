import streamlit as st
import random

# 1. Setup the Page
st.set_page_config(page_title="Cosmic Tarot", page_icon="✨")

# 2. Add some "Mood" with CSS
st.markdown("""
    <style>
    .main { background-color: #1a1a2e; color: #e94560; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4e31aa; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ Your Cosmic Bestie's Tarot")
st.subheader("What's on your mind, gorgeous?")

# 3. User Interaction
user_query = st.text_input("Ask the universe anything...", placeholder="e.g. Will I ever find my keys?")

if st.button("🔮 Reveal My Fate"):
    if user_query:
        with st.spinner("Channeling the energy..."):
            # UI LOGIC: Shuffle and Pick
            # (In your app, you'd call your Llama model here)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                # This is where the 'Card Image' would go
                st.image("https://placekitten.com/200/300", caption="The Magician (Upright)") 
            
            st.chat_message("assistant").write("Omg, okay so... the universe is basically saying...")
            # AI response goes here
    else:
        st.warning("You gotta ask a question first, babe!")
