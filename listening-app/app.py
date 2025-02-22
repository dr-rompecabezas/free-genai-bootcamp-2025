import os
import random

from dotenv import load_dotenv
from openai import OpenAI

import streamlit as st
import tempfile


# Load API keys from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Sample Toki Pona sentences with multiple valid translations
toki_pona_sentences = {
    "olin li pona": {
        "translations": [
            "Love is good",
            "Love is nice",
            "Love is simple",
            "Affection is positive",
        ],
        "context": "The word 'pona' can mean good/simple/positive, reflecting the subjective nature of the language",
    },
    "ona li lape": {
        "translations": [
            "They sleep",
            "She is sleeping",
            "He slept",
            "They are asleep",
            "It sleeps",
        ],
        "context": "Toki Pona doesn't specify gender, number, or tense - these are derived from context",
    },
    "moku mi li ike": {
        "translations": [
            "My food is bad",
            "My food is wrong",
            "My food is evil",
            "My meal is negative",
            "My eating is problematic",
        ],
        "context": "'ike' can mean bad/evil/wrong in moral, emotional, objective or subjective sense",
    },
    "sina olin": {
        "translations": [
            "You love",
            "You show affection",
            "You care",
            "You are loving",
        ],
        "context": "No tense is specified, and verbs can be interpreted as actions or states",
    },
    "mi jan pona sina": {
        "translations": [
            "I am your friend",
            "I am your good person",
            "I am a good person to you",
            "I am someone positive to you",
        ],
        "context": "'jan pona' literally means 'good person' but is commonly used to mean 'friend'",
    },
}

# Dictionary of Toki Pona words and their meanings
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

# Lesson context from the video transcript
lesson_transcript = """
toki pona is one of the most popular constructed languages out there, and in my opinion, that's because learning toki pona is a lot of fun.
it's a language with less than two hundred words. this restrictive vocabulary means that when speaking toki pona, talking about any complex subject involves describing what that thing is in simpler terms.
as jan Sonja has said, "if English is a thick novel, then toki pona is a haiku".

The name "toki pona" means "good language". the first word in the name is "toki", which generally means "communicate" or "communication".
you can also use toki as an interjection. saying "toki!" on its own is a way of announcing that communication is happening, as a way of starting a conversation.

all content words in toki pona have multiple functions like this. this is a very important part of how the language is able to work with such a small vocabulary.
it's important to remember that these multiple functions are not the same thing as a word having multiple meanings. all of these ideas encapsulated by toki fall under the large umbrella of "communication".
it's one single idea, but it corresponds to a large number of different English words, because English words are categorically more specific and precise than toki pona words.

Practice examples from the video:
1. "olin li pona" means "love is good" - showing how simple statements work with 'li'
2. "ona li lape" could mean "they sleep," "she is sleeping," "he slept" - demonstrating how toki pona doesn't specify gender, number, or tense
3. "moku mi li ike" means "my food is bad" - showing possession and the use of 'ike'
4. "sina olin" means "you love" - showing how 'li' is not used with 'sina'
5. "mi jan pona sina" means "I am your friend" - showing how 'jan pona' (good person) becomes 'friend'
"""


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
    """Evaluate user's English translation using GPT, considering multiple valid translations and context."""

    sentence_data = toki_pona_sentences[toki_pona_sentence]
    valid_translations = sentence_data["translations"]
    context = sentence_data["context"]

    # Format vocabulary and translations for better readability in the prompt
    vocab_context = "\n".join(
        [f"{word}: {meaning}" for word, meaning in toki_pona_vocab.items()]
    )
    translations_context = "\n".join(
        [f"{i + 1}. {translation}" for i, translation in enumerate(valid_translations)]
    )

    system_prompt = (
        f"Evaluate the accuracy of the user's Toki Pona translation to English:\n\n"
        f"The user has listened to the following Toki Pona sentence: {toki_pona_sentence}\n"
        f"This is a summary of the video lesson:\n{lesson_transcript}\n"
        f"These are some possible translations: \n{translations_context}\n\n"
        f"Additional Context: {context}\n"
        f"Key Word Definitions:\n{vocab_context}\n\n"
        f"Provide feedback on the accuracy of the user's translation, using the vocabulary meanings above.\n\n"
        f"Consider these key points when evaluating:\n\n"
        f"1. Toki Pona is intentionally minimalist and meanings are often contextual and fuzzy\n"
        f"2. Multiple translations can be valid for the same sentence \n"
        f"3. Focus on whether the core meaning is preserved, not exact wording\n"
    )

    user_input = f"My English Translation: {user_translation}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,  # Add some variability in responses while maintaining accuracy
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

# Debugging
# st.write("### Debugging:")
# st.write(f"Selected sentence: {st.session_state.selected_sentence}")
# st.write(f"Valid translations: {toki_pona_sentences[st.session_state.selected_sentence]}")
# st.write(f"Context: {toki_pona_sentences[st.session_state.selected_sentence]['context']}")

# User input and feedback
user_translation = st.text_input("Your English translation:")

if user_translation:
    feedback = check_translation(st.session_state.selected_sentence, user_translation)
    st.write("### Feedback:")
    st.write(feedback)
