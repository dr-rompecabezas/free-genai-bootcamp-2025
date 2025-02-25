"""Test configuration and shared fixtures."""

import os
from pathlib import Path
from typing import Generator

import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def app_path(project_root: Path) -> Path:
    """Return the path to app.py."""
    return project_root / "app.py"


@pytest.fixture(scope="session")
def models_dir(project_root: Path) -> Path:
    """Return the path to the models directory."""
    return project_root / "models"


@pytest.fixture(scope="session")
def templates_dir(project_root: Path) -> Path:
    """Return the path to the templates directory."""
    return project_root / "templates"


@pytest.fixture(scope="session")
def sitelen_pona_svgs_dir(project_root: Path) -> Path:
    """Return the path to the sitelen_pona_svgs directory."""
    return project_root / "sitelen_pona_svgs"


@pytest.fixture
def app(
    app_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Generator[AppTest, None, None]:
    """Initialize the app for testing with proper working directory."""
    # Change to app directory so relative paths work
    original_dir = os.getcwd()
    os.chdir(app_path.parent)

    # Initialize app
    at = AppTest.from_file(str(app_path))
    at.run()

    yield at

    # Restore original directory
    os.chdir(original_dir)


@pytest.fixture
def mock_recognizer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock the MobileNetSitelenPonaRecognizer to avoid loading real model."""

    class MockRecognizer:
        def __init__(self, *args, **kwargs):
            pass

        def load_templates(self, *args, **kwargs):
            return {"test": [0.5] * 1280}

        def process_image(self, *args, **kwargs):
            return [0.5] * 1280, []

        def compare_embeddings(self, *args, **kwargs):
            return 0.75

    monkeypatch.setattr("app.MobileNetSitelenPonaRecognizer", MockRecognizer)
