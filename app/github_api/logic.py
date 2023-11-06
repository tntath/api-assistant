import json
import os

from requests import get
from requests.models import Response

from config import DATA_DIR

URL = "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json"

save_path = os.path.join(DATA_DIR, "github_api_spec.json")


def fetch_github_api() -> Response | None:
    """Fetches the GitHub API spec from the GitHub repository.
    params:
        None
    returns:
        Response | None
    """
    response = get(URL)
    if response.status_code == 200:
        return response.json()


def save_github_api() -> None:
    """Saves the GitHub API spec to the DATA_DIR.
    params:
        None
    returns:
        None
    """
    data = fetch_github_api()
    with open(save_path, "w") as file:
        json.dump(data, file, indent=4)
