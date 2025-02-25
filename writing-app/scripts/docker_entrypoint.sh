#!/bin/bash
set -e

# First ensure the model exists
python scripts/ensure_model.py

# Then run the Streamlit app
exec streamlit run app.py
