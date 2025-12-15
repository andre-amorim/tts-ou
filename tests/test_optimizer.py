import pytest
from unittest.mock import MagicMock, patch
from optimizer import TextOptimizer

@pytest.fixture
def mock_genai():
    with patch("optimizer.genai") as mock:
        yield mock

@pytest.fixture
def mock_env_api_key(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "fake_key")

def test_optimizer_init(mock_genai, mock_env_api_key):
    opt = TextOptimizer()
    mock_genai.configure.assert_called_with(api_key="fake_key")
    mock_genai.GenerativeModel.assert_called_with("gemini-1.5-flash")

def test_optimizer_optimize(mock_genai, mock_env_api_key):
    opt = TextOptimizer()
    mock_model = mock_genai.GenerativeModel.return_value
    mock_response = MagicMock()
    mock_response.text = "Optimized text"
    mock_model.generate_content.return_value = mock_response
    
    text = "Some raw text"
    result = opt.optimize(text)
    
    assert result == "Optimized text"
    mock_model.generate_content.assert_called()
