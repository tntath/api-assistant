from fastapi import FastAPI, HTTPException

from app.github_api.assistant import GithubApiAssistant
from app.github_api.logic import save_github_api
from app.github_api.router import router as github_api_router

description = """
# GitHub API Assistant

This is a simple API that uses GPT-3 to answer questions about the GitHub API.

## How to use it?
* If you want to refresh the GitHub API file, go to /refresh-github-api.

* If you want to ask a question about the GitHub API, go to /ask?question=YOUR_QUESTION.

"""

app = FastAPI(title="GitHub API Assistant", description=description)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Greeting endpoint
    """
    return {
        "message": "Hello World! if you want to check the API through Swagger, go to /docs. "
    }


app.include_router(github_api_router, tags=["github-api"])
