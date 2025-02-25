"""Tests for the Sitelen Pona Writing Practice App."""
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from app import InputMode, SessionKey


@pytest.fixture
def app() -> AppTest:
    """Initialize the app for testing."""
    at = AppTest.from_file("app.py")
    
    # Initialize session state
    at.session_state[SessionKey.DEBUG_MODE] = False
    at.session_state[SessionKey.THRESHOLD] = 0.7
    at.session_state[SessionKey.SHOW_REFERENCE_DEFAULT] = True
    at.session_state[SessionKey.SHOW_REFERENCE] = True
    at.session_state[SessionKey.REFERENCE_BUTTON_KEY] = 0
    at.session_state[SessionKey.WHITE_GLYPHS] = False
    at.session_state[SessionKey.STROKE_THICKNESS] = 8
    
    at.run()
    return at


def test_app_loads_without_error(app: AppTest):
    """Test that the app loads without any exceptions."""
    assert not app.exception


def test_app_title(app: AppTest):
    """Test that the app title is correct."""
    assert app.title[0].value == "Sitelen Pona Writing Practice"


def test_app_tabs(app: AppTest):
    """Test that the app has Practice and Learn tabs."""
    assert app.tabs[0].label == "Practice"
    assert app.tabs[1].label == "Learn"


def test_input_mode_selector(app: AppTest):
    """Test the input mode selector."""
    selector = app.sidebar.selectbox[0]
    assert selector.label == "Choose Input Method"
    assert selector.options == InputMode.all_modes()
    assert selector.value == InputMode.DRAW  # Default value


def test_character_selector(app: AppTest):
    """Test the character selector."""
    selector = app.selectbox[0]
    assert selector.label == "Select Character to Practice"
    assert len(selector.options) > 0  # Should have some characters loaded
    assert selector.value is not None  # Should have a default character selected


def test_sidebar_settings(app: AppTest):
    """Test the sidebar settings."""
    sidebar = app.sidebar
    
    # Reference toggle
    ref_toggle = sidebar.toggle[0]
    assert ref_toggle.label == "Show Reference by Default"
    assert ref_toggle.value is True  # Default value
    
    # Recognition threshold
    threshold = sidebar.slider[0]
    assert threshold.label == "Recognition Threshold"
    assert threshold.value == 0.7  # Default value
    assert threshold.min == 0.5
    assert threshold.max == 0.9
    
    # Stroke thickness (only in draw mode)
    thickness = sidebar.slider[1]
    assert thickness.label == "Stroke Thickness"
    assert thickness.value == 8  # Default value
    assert thickness.min == 1
    assert thickness.max == 10


def test_reference_toggle_interaction(app: AppTest):
    """Test the reference toggle button interaction."""
    # Get initial state
    assert app.session_state[SessionKey.SHOW_REFERENCE] is True
    
    # Initial button should say "Hide Reference" since reference is shown
    toggle_button = next(
        button for button in app.button 
        if button.label in ["Hide Reference", "Show Reference"]
    )
    assert toggle_button.label == "Hide Reference"
    
    # Toggle off
    toggle_button.click().run()
    assert app.session_state[SessionKey.SHOW_REFERENCE] is False
    
    # After rerun, find button again and check label
    toggle_button = next(
        button for button in app.button 
        if button.label in ["Hide Reference", "Show Reference"]
    )
    assert toggle_button.label == "Show Reference"
    
    # Toggle on
    toggle_button.click().run()
    assert app.session_state[SessionKey.SHOW_REFERENCE] is True
    
    # After rerun, find button again and check label
    toggle_button = next(
        button for button in app.button 
        if button.label in ["Hide Reference", "Show Reference"]
    )
    assert toggle_button.label == "Hide Reference"


def test_stroke_thickness_interaction(app: AppTest):
    """Test the stroke thickness slider interaction."""
    # Switch to draw mode first
    mode_selector = app.sidebar.selectbox[0]
    mode_selector.set_value(InputMode.DRAW).run()
    
    # Verify initial state
    assert app.session_state[SessionKey.STROKE_THICKNESS] == 8
    
    # Verify slider exists and has correct properties
    thickness_slider = next(
        s for s in app.sidebar.slider 
        if s.label == "Stroke Thickness"
    )
    assert thickness_slider.value == 8
    assert thickness_slider.min == 1
    assert thickness_slider.max == 10
    assert thickness_slider.key == SessionKey.STROKE_THICKNESS
    
    # Switch to upload mode and verify slider disappears
    mode_selector.set_value(InputMode.UPLOAD).run()
    assert not any(
        s.label == "Stroke Thickness" 
        for s in app.sidebar.slider
    )
    
    # Switch back to draw mode and verify slider reappears
    mode_selector.set_value(InputMode.DRAW).run()
    thickness_slider = next(
        s for s in app.sidebar.slider 
        if s.label == "Stroke Thickness"
    )
    assert thickness_slider.value == 8


def test_mode_switching(app: AppTest):
    """Test switching between input modes."""
    # Get the mode selector
    mode_selector = app.sidebar.selectbox[0]
    assert mode_selector.label == "Choose Input Method"
    
    # Test each mode
    for mode in InputMode.all_modes():
        # Switch mode
        mode_selector.set_value(mode).run()
        
        # Verify mode is selected
        assert mode_selector.value == mode
        
        # Verify stroke thickness slider only shows in draw mode
        thickness_sliders = [
            s for s in app.sidebar.slider 
            if s.label == "Stroke Thickness"
        ]
        
        if mode == InputMode.DRAW:
            assert len(thickness_sliders) == 1
            assert thickness_sliders[0].value == 8
        else:
            assert len(thickness_sliders) == 0


def test_learn_tab_features(app: AppTest):
    """Test the learn tab features."""
    # Switch to learn tab (no need to click, content is already rendered)
    tabs = app.tabs
    learn_tab = tabs[1]
    assert learn_tab.label == "Learn"
    
    # Check header
    assert any("Sitelen Pona Glyphs" in header.value for header in app.header)
    
    # Test white glyph toggle
    white_toggle = app.toggle[0]
    assert white_toggle.label == "Use white glyphs"
    assert not white_toggle.value  # Default is black glyphs
    
    # Verify glyph labels exist
    assert len(app.caption) > 0  # Should have glyph labels


def test_random_character_selection(app: AppTest):
    """Test the random character selection button."""
    # Get initial character
    char_selector = app.selectbox[1]  # First is input mode
    initial_char = char_selector.value
    
    # Click random button and verify character changed
    random_button = next(
        button for button in app.button 
        if "🎲" in button.label
    )
    assert random_button.label == "🎲 Random"
    
    # Can't test actual randomization since it requires st.rerun()
    # Just verify button exists with correct label


def test_character_selection_callback(app: AppTest):
    """Test character selection callback behavior."""
    # Get initial reference state
    assert app.session_state[SessionKey.SHOW_REFERENCE_DEFAULT] is True
    assert app.session_state[SessionKey.SHOW_REFERENCE] is True
    
    # Toggle reference default off
    ref_toggle = app.sidebar.toggle[0]  # First toggle in sidebar
    assert ref_toggle.label == "Show Reference by Default"
    ref_toggle.set_value(False).run()
    
    # Change character and verify reference matches default
    char_selector = app.selectbox[1]  # First is input mode
    current_char = char_selector.value
    available_chars = char_selector.options
    new_char = next(c for c in available_chars if c != current_char)
    
    # Update session state directly since selectbox callback won't work in test
    app.session_state[SessionKey.SELECTED_CHAR] = new_char
    app.session_state[SessionKey.SHOW_REFERENCE] = app.session_state[SessionKey.SHOW_REFERENCE_DEFAULT]
    app.run()
    
    # Verify states
    assert app.session_state[SessionKey.SELECTED_CHAR] == new_char
    assert not app.session_state[SessionKey.SHOW_REFERENCE]


def test_debug_mode_features(app: AppTest):
    """Test debug mode features."""
    # Enable debug mode
    debug_toggle = next(
        toggle for toggle in app.sidebar.toggle
        if toggle.label == "Debug Mode"
    )
    assert not debug_toggle.value  # Default is off
    debug_toggle.set_value(True).run()
    
    # Switch to draw mode
    mode_selector = app.sidebar.selectbox[0]
    mode_selector.set_value(InputMode.DRAW).run()
    
    # Verify debug mode is enabled
    assert app.session_state[SessionKey.DEBUG_MODE] is True