import pytest
import requests
from unittest.mock import Mock, patch
from app.services.api_client import APIClient
from app.exceptions import PokemonAPIException, PokemonNotFoundException


@pytest.fixture
def api_client():
    return APIClient(base_url="https://test-api.com")


def test_successful_get(api_client):
    mock_response = Mock()
    mock_response.json.return_value = {"name": "pikachu"}
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response) as mock_get:
        result = api_client.get("pokemon/pikachu")

        assert result == {"name": "pikachu"}
        mock_get.assert_called_once_with("https://test-api.com/pokemon/pikachu")


def test_timeout_error(api_client):
    with patch('requests.get', side_effect=requests.Timeout):
        with pytest.raises(PokemonAPIException, match="Request timed out"):
            api_client.get("pokemon/pikachu")

