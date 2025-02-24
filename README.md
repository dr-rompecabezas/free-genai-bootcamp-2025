# GenAI Bootcamp 2025: Toki Pona AI-Enhanced Language Learning Experiments

This repository contains assignments completed during ExamPro's free GenAI Bootcamp. Be aware that **this code is not meant for production use**. The git tags only serve as a record of progress through the bootcamp. Similarly, GitHub issues have been used to help instructors quickly reference the commits related to a particular assignment.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Directory Structure

- [🎨 `/writing-app` directory](#-writing-app-directory)
- [🎧 `/listening-app` directory](#-listening-app-directory)
- [🪢 `/lang-portal` directory](#-lang-portal-directory)
- [🧭 `/genai-architecting` directory](#-genai-architecting-directory)
- [🔭 `/sentence-constructor` directory](#-sentence-constructor-directory)
- [🧪 `/dev-tools` directory](#-dev-tools-directory)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
## 🎨 `/writing-app` directory

The `/writing-app` directory contains a Streamlit-based character recognition application for Sitelen Pona (Toki Pona's writing system). Key features include:

- Real-time character recognition using MediaPipe's Image Embedder with MobileNetV3-Small
- Multiple input methods: interactive canvas, webcam capture, and file upload
- Cosine similarity-based recognition with adjustable confidence threshold
- Debug mode for visualizing image preprocessing and embedding comparisons
- Interactive canvas for drawing practice with immediate feedback
- Comprehensive grid view of all Sitelen Pona glyphs with dark mode support
- SVG-based rendering for crisp, scalable character display
- Responsive design with intuitive user interface

The application demonstrates effective use of modern computer vision techniques for handwritten character recognition in language education, with an emphasis on user control and transparency in the recognition process.

## 🎧 `/listening-app` directory

The `listening-app` directory contains a Streamlit-based application featuring:

- Interactive translation practice with AI-powered feedback
- Text-to-speech capabilities using OpenAI's TTS API
- GPT prompt construction for context-dependent translations
- Utility tool for processing YouTube transcripts to support NLP tasks

The application demonstrates practical use of Large Language Models (GPT) and Text-to-Speech technology in language education.

## 🪢 `/lang-portal` directory

This directory contains the source code for the language learning platform. It has been rebuilt twice. The current backend is a FastAPI application with 100% test coverage for the endpoints, CRUD operations, Pydantic models, and SQLAlchemy models.

The frontend was removed as it is being rebuilt. See Issue #3 for details.

To see the older builds, check out the `flask-react-final` and `fastapi-vue-final` tags:

```sh
git checkout -b flask-react-final
git checkout -b fastapi-vue-final
```

The first migration experience was documented in the `/dev-tools` directory as a homework assignment. The second, current rebuild was documented in the detailed git commit messages.

## 🧭 `/genai-architecting` directory

The `/genai-architecting` directory contains solution architecting assignments. It is meant to serve as a reference for the architecture of the GenAI-powered language learning platform that is being built.

## 🔭 `/sentence-constructor` directory

The `/sentence-constructor` directory contains a report on the exploration of specific large language models' baseline capabilities to act as language tutors using simple prompts and feedback.

## 🧪 `/dev-tools` directory

The `/dev-tools` directory contains detailed notes on the use of Windsurf to migrate the application from Flask and React to FastAPI and Vue.
