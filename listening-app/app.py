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
    """Evaluate user's English translation using GPT, with key word definitions as context."""

    expected_translation = toki_pona_sentences.get(
        toki_pona_sentence, "No reference available."
    )

    toki_pona_vocab = {
        "toki": "communicate",
        "pona": "good",
        "ike": "bad",
        "jan": "person",
        "li": "[verb-marking particle]",
        "moku": "food; eat",
        "lape": "sleep",
        "olin": "love",
        "ona": "them, her, him, it",
        "mi": "me, us",
        "sina": "you",
    }

    # Format vocabulary for better readability in the prompt
    vocab_context = "\n".join(
        [f"{word}: {meaning}" for word, meaning in toki_pona_vocab.items()]
    )

    system_prompt = (
        f"Evaluate the accuracy of the user's Toki Pona translation to English:\n\n"
        f"The user has listened to the following Toki Pona sentence: {toki_pona_sentence}\n"
        f"This is the expected translation: {expected_translation}\n\n"
        f"Key Word Definitions:\n{vocab_context}\n\n"
        f"Provide feedback on the accuracy of the user's translation, using the vocabulary meanings above. "
        f"If the translation is incorrect, suggest a hint before revealing the correct answer."
    )

    user_input = f"My English Translation: {user_translation}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
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

# Ensure sentence stays the same for the current attempt
if "selected_sentence" not in st.session_state:
    st.session_state.selected_sentence = random.choice(list(toki_pona_sentences.keys()))

# Generate and play audio
audio_file = generate_audio(st.session_state.selected_sentence)
if audio_file:
    st.audio(audio_file, format="audio/mp3")

# User input and feedback
user_translation = st.text_input("Your English translation:")

if user_translation:
    feedback = check_translation(st.session_state.selected_sentence, user_translation)
    st.write("### Feedback:")
    st.write(feedback)
