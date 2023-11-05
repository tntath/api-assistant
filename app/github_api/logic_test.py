import os
from unittest.mock import Mock

import pytest

from app.github_api.logic import fetch_github_api, save_github_api
from config import DATA_DIR

save_path = os.path.join(DATA_DIR, "github_api_spec.json")


@pytest.fixture
def mock_get_requests(monkeypatch):
    mock = Mock()
    monkeypatch.setattr("app.github_api.logic.get", mock)
    return mock


class TestFetchGithubApi:
    def test_fetch_github_api(self, mock_get_requests) -> None:
        mock_get_requests.return_value.status_code = 200
        mock_get_requests.return_value.json.return_value = {"mock_key": "mock_response"}

        data = fetch_github_api()

        mock_get_requests.assert_called_once_with(
            "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json"
        )
        assert data is not None
        assert "mock_key" in data
        assert data["mock_key"] == "mock_response"

    def test_saved_github_api(
        self,
    ) -> None:
        if not os.path.exists(save_path):
            save_github_api()

        with open(save_path, "r") as file:
            data = file.read()

        assert data is not None
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
