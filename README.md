# Toki Pona AI-Enhanced Language Learning Platform

This repository contains assignments completed during ExamPro's free GenAI Bootcamp. Be aware that this code is not meant for production use. The releases and git tags are meant to serve as a record of progress through the boot camp. Similarly, GitHub issues have been used to help instructors quickly reference the commits related to a particular assignment.

This README explains the top-level repository structure. Additional README files are provided throughout the repository to provide additional context.

## `/lang-portal` directory

This directory contains the source code for the language learning platform. It has been rebuilt twice. The current backend is a FastAPI application with 100% test coverage for the endpoints, CRUD operations, Pydantic models, and SQLAlchemy models.

The frontend was removed as it is being rebuilt. See Issue #3 for details.

To see the older builds, check out the `flask-react-final` and `fastapi-vue-final` tags (see details below).

### Original Codebase in Flask and React

The `lang-portal` directory originally contained a Flask backend and a React frontend, copied over as-is, from the instructor's repository.

The last commit before switching to FastAPI and Vue is tagged as `flask-react-final`.

```sh
git checkout flask-react-final
```

### Migration to FastAPI and Vue

The codebase was then migrated to FastAPI and Vue, using the Windsurf code editor, as part of a learning exercise to test the capabilities of the new generation of AI-powered code editors. The last commit after completing the migration is tagged as `fastapi-vue-final`.

```sh
git checkout fastapi-vue-final
```

This migration experience was documented in the `/dev-tools` directory.

## `/genai-architecting` directory

The `/genai-architecting` directory contains solution architecting assignments. It is meant to serve as a reference for the architecture of the GenAI-powered language learning platform that is being built.

## `/sentence-constructor` directory

The `/sentence-constructor` directory contains a report on the exploration of specific large language models' baseline capabilities to act as language tutors using simple prompts and feedback.

## `/dev-tools` directory

The `/dev-tools` directory contains detailed notes on the use of Windsurf to migrate the application from Flask and React to FastAPI and Vue.
