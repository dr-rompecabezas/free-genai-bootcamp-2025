import os
import random

from dotenv import load_dotenv
from openai import OpenAI

import streamlit as st
import tempfile


# Load API keys from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Sample Toki Pona sentences and expected translations
toki_pona_sentences = {
    "toki pona li toki pi pona.": "Toki Pona is the language of good.",
    "mi wile e moku.": "I want food.",
    "sina sona ala sona e toki pona?": "Do you know Toki Pona?",
    "jan li tawa tomo.": "The person goes to the house.",
    "mi moku e kili.": "I eat fruit.",
}


def generate_audio(text):
    """Generate speech from text using OpenAI's TTS API."""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # Change voice if needed
            input=text,
        )
        # Save as a temporary MP3 file
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_audio_file.write(response.content)
        temp_audio_file.close()
        return temp_audio_file.name  # Return file path
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None


def check_translation(toki_pona_sentence, user_translation):
    """Evaluate user's English translation using GPT."""
    expected_translation = toki_pona_sentences.get(
        toki_pona_sentence, "No reference available."
    )

    prompt = (
        f"Evaluate the accuracy of this Toki Pona translation:\n\n"
        f"Toki Pona: {toki_pona_sentence}\n"
        f"User's Translation: {user_translation}\n"
        f"Expected Translation: {expected_translation}\n\n"
        f"Provide feedback: is the translation correct? If incorrect, suggest improvements."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error checking translation: {e}"


# Streamlit UI
st.title("Toki Pona AI Learning Prototype")

# Embedded lesson video
st.header("Step 1: Watch the Lesson")
st.video("https://www.youtube.com/watch?v=2EZihKCB9iw")
st.write(
    "Watch this short introduction to Toki Pona before proceeding to the listening activity."
)

# Listening Exercise
st.header("Step 2: Listening Activity")
st.write("Listen to the sentence and enter your translation:")

# Generate and play audio
selected_sentence = random.choice(list(toki_pona_sentences.keys()))
audio_file = generate_audio(selected_sentence)
if audio_file:
    st.audio(audio_file, format="audio/mp3")

# User input
user_translation = st.text_input("Your English translation:")

if user_translation:
    feedback = check_translation(selected_sentence, user_translation)
    st.write("### Feedback:")
    st.write(feedback)
