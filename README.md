# GenAI Bootcamp 2025: Building an AI-enhanced Language Learning Platform

This repository contains assignments completed during the ExamPro's free GenAI Bootcamp. Be aware that no code in here is **not meant for production use**. The releases and git tags are meant to serve as a record of progress through the bootcamp. Similarly, GitHub issues have been used only as a way to help instructors quickly reference the commits related to a particular assignment.

This README explains the project structure, starting with the `lang-portal` directory. Additional README files are provided throughout the codebase in context.

## /lang-portal directory

This is the main repository of the language learning platform. It originally contained a Flask backend and a React frontend, copied over as-is, from the instructor's repository. The last commit before switching to FastAPI and Vue is tagged as `flask-react-final`. To view the old implementation in a detached HEAD state, run:

```bash
git checkout flask-react-final
```

The codebase was then migrated to FastAPI and Vue, using the Windsurf code editor, as part of a learning exercise to test the capabilities of the new generation of AI-powered code editors.

TODO: The migration experience will be documented in a `/dev-tools` directory.

## /genai-architecting directory

The `/genai-architecting` directory contains solution architecting assignments. It is meant to serve as a reference for the architecture of the GenAI-powered language learning platform that is being built.

## /sentence-constructor directory

The `/sentence-constructor` directory contains a report on the exploration of specific large language models' baseline capabilities to act as language tutors using simple prompts and feedback.
