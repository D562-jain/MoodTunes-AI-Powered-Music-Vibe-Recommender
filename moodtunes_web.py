import streamlit as st
st.set_page_config(page_title="MoodTunes", page_icon="🎧")

import random
import speech_recognition as sr
import pyttsx3
from textblob import TextBlob
import threading




# -------------------------------------
# 🎵 Mood-based music playlist
# -------------------------------------
mood_map = {
    "positive": ["🎉 Try upbeat pop or dance hits!", "🔥 Hype vibes? Go EDM!"],
    "negative": ["💤 Chill with lo-fi beats or soft piano.", "🌧️ Try rainy-day jazz."],
    "neutral": ["☁️ Maybe ambient or indie folk?", "🎧 Just vibin’? Try instrumental mixes."]
}

emoji_map = {
    "positive": "😄",
    "negative": "😢",
    "neutral": "😐"
}

mood_links = {
    "positive": [
        ("Happy - Pharrell", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
        ("Gangnam Style", "https://www.youtube.com/watch?v=9bZkp7q19f0"),
        ("Shape of You - Ed Sheeran", "https://www.youtube.com/watch?v=JGwWNGJdvx8"),
        ("Uptown Funk - Bruno Mars", "https://www.youtube.com/watch?v=OPf0YbXqDm0"),
        ("Despacito", "https://www.youtube.com/watch?v=kJQP7kiw5Fk")
    ],
    "negative": [
        ("Lo-fi chill beats", "https://www.youtube.com/watch?v=DWcJFNfaw9c"),
        ("Hello - Adele", "https://www.youtube.com/watch?v=YQHsXMglC9A"),
        ("See You Again - Wiz Khalifa", "https://www.youtube.com/watch?v=RgKAFK5djSk"),
        ("Love the Way You Lie", "https://www.youtube.com/watch?v=uelHwf8o7_U"),
        ("I Will Always Love You", "https://www.youtube.com/watch?v=3JWTaaS7LdU")
    ],
    "neutral": [
        ("Chillhop Radio", "https://www.youtube.com/watch?v=5qap5aO4i9A"),
        ("River Flows in You", "https://www.youtube.com/watch?v=lTRiuFIWV54"),
        ("Believer - Imagine Dragons", "https://www.youtube.com/watch?v=VPRjCeoBqrI"),
        ("Stressed Out - TOP", "https://www.youtube.com/watch?v=pXRviuL6vMY"),
        ("Can't Stop The Feeling", "https://www.youtube.com/watch?v=fLexgOxsZu0")
    ]
}

# -------------------------------------
# 🔊 Text-to-speech engine
# -------------------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass  # or handle with logging

# -------------------------------------
# 🔍 Mood analysis using TextBlob
# -------------------------------------
def analyze_mood(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

# -------------------------------------
# 🎙️ Voice input
# -------------------------------------
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout=3)  # Reduced timeout
        return recognizer.recognize_google(audio)


# -------------------------------------
# 🎨 Lo-fi Animated Background
# -------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://your-optimized-image-url.com");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------
# 🎧 Main App UI
# -------------------------------------

st.title("🎧 MoodTunes – Music Vibe Recommender")
st.write("Tell me how you're feeling and I’ll suggest the perfect vibe 💫")

input_method = st.radio("Choose input method:", ["Type", "Talk 🎤"])
user_input = ""

if input_method == "Type":
    user_input = st.text_input("How are you feeling right now?")
    if st.button("Get Suggestion"):
        if user_input:
           with st.spinner("Analyzing your mood..."):
            mood = analyze_mood(user_input)

            suggestion = random.choice(mood_map[mood])
            st.markdown(f"## Mood: {emoji_map[mood]}")
            st.success(f"🎵 Suggestion: {suggestion}")
            st.subheader("🎧 Suggested Playlist:")
            for title, url in mood_links[mood]:
                st.link_button(f"▶️ {title}", url)

            threading.Thread(target=speak, args=(suggestion,)).start()

elif input_method == "Talk 🎤":
    if st.button("Speak Now"):
        try:
            st.info("🎙️ Listening...")
            user_input = get_voice_input()
            st.write(f"You said: *{user_input}*")
            mood = analyze_mood(user_input)
            suggestion = random.choice(mood_map[mood])
            st.markdown(f"## Mood: {emoji_map[mood]}")
            st.success(f"🎵 Suggestion: {suggestion}")
            st.subheader("🎧 Suggested Playlist:")
            for title, url in mood_links[mood]:
                st.markdown(f"- [{title}]({url})")
            threading.Thread(target=speak, args=(suggestion,)).start()
        except Exception as e:
            st.error(f"Oops: {str(e)}")

