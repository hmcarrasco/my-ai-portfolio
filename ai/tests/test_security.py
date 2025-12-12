import pytest
from fastapi import HTTPException
import ai.api.security as security_module


class TestSecurity:
    """Test suite for API security functions."""

    def test_verify_api_key_valid(self, monkeypatch):
        """Test API key verification with valid key."""
        monkeypatch.setattr(security_module, "CHATBOT_API_KEY", "test-chatbot-key")
        result = security_module.verify_api_key("test-chatbot-key")
        assert result == "test-chatbot-key"

    def test_verify_api_key_invalid(self, monkeypatch):
        """Test API key verification with invalid key."""
        monkeypatch.setattr(security_module, "CHATBOT_API_KEY", "test-chatbot-key")
        with pytest.raises(HTTPException) as exc_info:
            security_module.verify_api_key("wrong-key")
        
        assert exc_info.value.status_code == 401
        assert "Invalid API Key" in exc_info.value.detail

    def test_verify_api_key_not_configured(self, monkeypatch):
        """Test API key verification when key is not configured."""
        monkeypatch.setattr(security_module, "CHATBOT_API_KEY", None)
        with pytest.raises(HTTPException) as exc_info:
            security_module.verify_api_key("any-key")
        
        assert exc_info.value.status_code == 500
        assert "not configured" in exc_info.value.detail

    @pytest.mark.parametrize("api_key", [
        "sk-test-key-123",
        "very-long-api-key-with-special-chars-!@#$%",
        "short",
    ])
    def test_verify_api_key_various_formats(self, api_key, monkeypatch):
        """Test API key verification with various key formats."""
        monkeypatch.setattr(security_module, "CHATBOT_API_KEY", api_key)
        result = security_module.verify_api_key(api_key)
        assert result == api_key
