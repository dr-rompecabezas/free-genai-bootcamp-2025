from src.toki_pona_api.config import Settings

def test_validate_cors_origins():
    """Test CORS origins validation with both string and list inputs."""
    # Test with JSON string
    json_input = '["http://localhost:3000", "http://example.com"]'
    result = Settings.validate_cors_origins(json_input)
    assert isinstance(result, list)
    assert result == ["http://localhost:3000", "http://example.com"]
    
    # Test with list input
    list_input = ["http://localhost:3000"]
    result = Settings.validate_cors_origins(list_input)
    assert result == list_input
