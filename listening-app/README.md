# Toki Pona AI Learning Prototype

An interactive learning tool that helps you practice Toki Pona translations with AI-powered feedback and audio generation.

## Features

- Watch an introductory Toki Pona lesson
- Practice translating Toki Pona sentences to English
- Listen to AI-generated pronunciations
- Get instant feedback on your translations using GPT-4

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- `uv` package manager (recommended) or `pip`

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/dr-rompecabezas/free-genai-bootcamp-2025)
   cd toki-pona-ai
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # or
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:

   Using `uv` (recommended):

   ```bash
   uv sync
   ```

   Or using `pip`:

   ```bash
   pip install pip-tools
   pip-compile pyproject.toml  # Generate requirements.txt from pyproject.toml
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:

   ```text
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the App

Start the Streamlit app:

```bash
python -m streamlit run app.py
```

The app will open in your default web browser. If it doesn't open automatically, visit `http://localhost:8501`.

## Usage

1. Watch the introductory video to learn about Toki Pona basics
2. Listen to the randomly selected Toki Pona sentence
3. Enter your English translation in the text input
4. Get instant feedback on your translation accuracy

## Note

This is a prototype application. The current version includes a limited set of Toki Pona sentences for practice. Make sure you have a stable internet connection as the app requires access to OpenAI's API for translation feedback and audio generation.

## Version Control

- The `uv.lock` file is committed to the repository to ensure reproducible builds
- If using pip, the generated `requirements.txt` should also be committed
- Do not commit the `.env` file as it contains sensitive API keys
