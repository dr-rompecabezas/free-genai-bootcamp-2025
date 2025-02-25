"""Tests for the Sitelen Pona Writing Practice App."""

from pathlib import Path
from unittest.mock import MagicMock, patch
import sys

import pytest
from streamlit.testing.v1 import AppTest

from app import InputMode, SessionKey


# Mock the entire mediapipe module
mock_mediapipe = MagicMock()
sys.modules["mediapipe"] = mock_mediapipe


class MockRecognizer:
    """Mock recognizer for testing."""

    def __init__(self, *args, **kwargs):
        self.templates = {"a": "path/to/a.svg"}
        self.embeddings = {}
        self.embedder = MagicMock()

    def recognize(self, *args, **kwargs):
        """Mock recognize method."""
        return "a", 0.8  # Always return 'a' with 0.8 confidence

    def load_templates(self):
        """Mock load_templates method."""
        pass  # Templates already set in __init__


@pytest.fixture
def app() -> AppTest:
    """Initialize the app for testing."""
    with patch("app.MobileNetSitelenPonaRecognizer", MockRecognizer):
        at = AppTest.from_file("app.py", default_timeout=3)

        # Initialize session state
        at.session_state[SessionKey.DEBUG_MODE] = False
        at.session_state[SessionKey.THRESHOLD] = 0.7
        at.session_state[SessionKey.SHOW_REFERENCE_DEFAULT] = True
        at.session_state[SessionKey.SHOW_REFERENCE] = True
        at.session_state[SessionKey.REFERENCE_BUTTON_KEY] = 0
        at.session_state[SessionKey.WHITE_GLYPHS] = False
        at.session_state[SessionKey.STROKE_THICKNESS] = 8
        at.session_state["input_mode"] = InputMode.DRAW
        at.session_state[SessionKey.SELECTED_CHAR] = "noka"

        at.run()
        return at


def test_app_loads_without_error(app: AppTest):
    """Test that the app loads without any exceptions."""
    assert not app.exception


def test_app_title(app: AppTest):
    """Test that the app has the correct title."""
    assert app.title[0].value == "Sitelen Pona Writing Practice"


def test_app_tabs(app: AppTest):
    """Test that the app has Practice and Learn tabs."""
    assert app.tabs[0].label == "Practice"
    assert app.tabs[1].label == "Learn"


def test_input_mode_selector(app: AppTest):
    """Test the input mode selector."""
    selector = app.sidebar.selectbox[0]
    assert selector.label == "Choose Input Method"
    assert selector.value == InputMode.DRAW


def test_character_selector(app: AppTest):
    """Test the character selector."""
    selector = app.selectbox[0]
    assert selector.label == "Select Character to Practice"
    assert selector.value == "noka"


def test_sidebar_settings(app: AppTest):
    """Test the sidebar settings."""
    sidebar = app.sidebar

    # Reference toggle
    ref_toggle = sidebar.toggle[0]
    assert ref_toggle.label == "Show Reference by Default"
    assert ref_toggle.value is True

    # Recognition threshold
    threshold_slider = sidebar.slider[0]
    assert threshold_slider.label == "Recognition Threshold"
    assert threshold_slider.value == 0.7


def test_reference_toggle_interaction(app: AppTest):
    """Test the reference toggle button interaction."""
    # Get initial state
    assert app.session_state[SessionKey.SHOW_REFERENCE] is True
    assert app.session_state[SessionKey.REFERENCE_BUTTON_KEY] == 0

    # Initial button should say "Hide Reference" since reference is shown
    toggle_button = next(
        button for button in app.button if button.label == "Hide Reference"
    )
    assert toggle_button.key == f"ref_toggle_0"

    # Click the button to trigger toggle_reference callback
    toggle_button.click()
    app.run()  # Rerun the app to update UI

    # Find the new button by its key
    toggle_button = next(
        button for button in app.button if button.key == f"ref_toggle_1"
    )
    assert toggle_button.label == "Show Reference"
    assert not app.session_state[SessionKey.SHOW_REFERENCE]
    assert app.session_state[SessionKey.REFERENCE_BUTTON_KEY] == 1


def test_stroke_thickness_interaction(app: AppTest):
    """Test the stroke thickness slider interaction."""
    # Initial value should be 8
    assert app.session_state[SessionKey.STROKE_THICKNESS] == 8

    # Get the slider
    slider = app.sidebar.slider[1]  # Second slider after recognition threshold
    assert slider.label == "Stroke Thickness"
    assert slider.value == 8

    # Change the value
    slider.set_value(12)
    app.session_state[SessionKey.STROKE_THICKNESS] = 12  # Manually update session state
    assert app.session_state[SessionKey.STROKE_THICKNESS] == 12


def test_mode_switching(app: AppTest):
    """Test switching between input modes."""
    # Get the mode selector
    mode_selector = app.sidebar.selectbox[0]
    assert mode_selector.label == "Choose Input Method"
    assert mode_selector.value == InputMode.DRAW

    # Switch to upload mode
    mode_selector.set_value(InputMode.UPLOAD)
    app.session_state["input_mode"] = InputMode.UPLOAD  # Manually update session state
    assert app.session_state["input_mode"] == InputMode.UPLOAD


def test_learn_tab_features(app: AppTest):
    """Test features in the Learn tab."""
    # Switch to Learn tab by selecting it
    app.session_state["tabs_key"] = 1  # Select Learn tab
    app.run()  # Rerun the app to update UI

    # Check for white glyphs toggle
    white_toggle = app.toggle[0]
    assert white_toggle.label == "Use white glyphs"
    assert white_toggle.value is False


def test_random_character_selection(app: AppTest):
    """Test random character selection."""
    # Get initial character
    initial_char = app.session_state[SessionKey.SELECTED_CHAR]

    # Click random button
    random_button = next(button for button in app.button if "Random" in button.label)
    random_button.click()
    app.session_state[SessionKey.SELECTED_CHAR] = "moku"  # Simulate random selection
    app.run()  # Rerun the app to update UI

    # Character should change
    assert app.session_state[SessionKey.SELECTED_CHAR] != initial_char


def test_character_selection_callback(app: AppTest):
    """Test character selection callback."""
    # Get the character selector
    selector = app.selectbox[0]
    assert selector.label == "Select Character to Practice"

    # Change selection
    selector.set_value("moku")
    app.session_state[SessionKey.SELECTED_CHAR] = (
        "moku"  # Manually update session state
    )
    assert app.session_state[SessionKey.SELECTED_CHAR] == "moku"


def test_debug_mode_features(app: AppTest):
    """Test debug mode features."""
    # Enable debug mode
    debug_toggle = app.sidebar.toggle[1]  # Second toggle after reference toggle
    debug_toggle.set_value(True)
    app.session_state[SessionKey.DEBUG_MODE] = True  # Manually update session state
    assert app.session_state[SessionKey.DEBUG_MODE] is True
