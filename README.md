# GenAI Bootcamp 2025: Toki Pona AI-Enhanced Language Learning Experiments

This repository contains assignments completed during ExamPro's free GenAI Bootcamp. The final project is hosted at <https://github.com/think-elearn/toki-pona-ai>.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
## Directory Structure

- [🤖 `/agentic-workflow` directory](#-agentic-workflow-directory)
- [🎨 `/writing-app` directory](#-writing-app-directory)
- [🎧 `/listening-app` directory](#-listening-app-directory)
- [✌️ `/signing-app` directory](#-signing-app-directory)
- [🪢 `/lang-portal` directory](#-lang-portal-directory)
- [🔮 `/opea-comps` directory](#-opea-comps-directory)
- [🧭 `/genai-architecting` directory](#-genai-architecting-directory)
- [🔭 `/sentence-constructor` directory](#-sentence-constructor-directory)
- [🧪 `/dev-tools` directory](#-dev-tools-directory)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## 🤖 `/agentic-workflow` directory

The `/agentic-workflow` directory contains a Toki Pona Learning Assistant that leverages AI to create an interactive language learning experience. Key features include:

- **Video-Based Learning**: Integration with YouTube's Data API to discover and analyze Toki Pona learning content
- **AI-Powered Analysis**: Uses Claude to process video transcripts, extract vocabulary, and generate customized quizzes
- **Interactive Learning Flow**: Structured workflow for video selection, content study, and knowledge testing at multiple difficulty levels

The application demonstrates practical use of modern AI technologies (Claude, YouTube APIs) for creating an engaging language learning experience, with emphasis on vocabulary extraction and adaptive quiz generation.

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

## ✌️ `/signing-app` directory

The `/signing-app` directory contains the Luka Pona Signing Learning App, a prototype application that helps users learn sign language through computer vision and machine learning. Key features include:

- Real-time hand tracking and landmark detection using MediaPipe
- Dynamic Time Warping (DTW) for comparing learner signs with templates
- Detailed feedback with similarity scores and areas for improvement
- Visual analysis tools including side-by-side comparisons and heatmaps
- GIF-based recording and playback for sign comparisons

The application demonstrates practical use of computer vision and gesture recognition in language education, with an emphasis on providing meaningful feedback to learners.

## 🪢 `/lang-portal` directory

This directory contains the source code for the language learning platform. It has been rebuilt twice. The current backend is a FastAPI application with 100% test coverage for the endpoints, CRUD operations, Pydantic models, and SQLAlchemy models.

The frontend was removed as it is being rebuilt. See Issue #3 for details.

To see the older builds, check out the `flask-react-final` and `fastapi-vue-final` tags:

```sh
git checkout -b flask-react-final
git checkout -b fastapi-vue-final
```

The first migration experience was documented in the `/dev-tools` directory as a homework assignment. The second, current rebuild was documented in the detailed git commit messages.

## 🔮 `/opea-comps` directory

The `/opea-comps` directory contains experiments with the OPEA (Open Enterprise AI) ChatQnA Megaservice. The project documents two deployment attempts:

- Mac M1 Chip adaptation with platform emulation for x86 containers
- AWS EC2 deployment on an m7i.4xlarge instance with Intel Xeon processor

Key implementation details include:

- Docker configuration adaptations for ARM architecture compatibility
- Environment variable setup and networking configuration
- Model selection optimized for hardware constraints
- Microservices setup including embedding, retrieval, and LLM components
- Troubleshooting solutions for common deployment issues

The project demonstrates the challenges and solutions involved in deploying complex GenAI microservice architectures across different computing environments, with detailed documentation of both successes and limitations.

## 🧭 `/genai-architecting` directory

The `/genai-architecting` directory contains solution architecting assignments. It is meant to serve as a reference for the architecture of the GenAI-powered language learning platform that is being built.

## 🔭 `/sentence-constructor` directory

The `/sentence-constructor` directory contains a report on the exploration of specific large language models' baseline capabilities to act as language tutors using simple prompts and feedback.

## 🧪 `/dev-tools` directory

The `/dev-tools` directory contains detailed notes on the use of Windsurf to migrate the application from Flask and React to FastAPI and Vue.
