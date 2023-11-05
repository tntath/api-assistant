from fastapi import APIRouter, HTTPException
from app.github_api.assistant import GithubApiAssistant
from app.github_api.fetch import save_github_api
from app.utils.embeddings import Embeddings

router = APIRouter()


@router.get("/refresh-github-api")
async def refresh_github_api_file() -> dict[str, str]:
    """
    Refreshes the GitHub API file
    """
    save_github_api()
    return {"message": "GitHub API refreshed!"}


@router.get("/reresh-embeddings")
async def refresh_embeddings() -> dict[str, str]:
    """
    Refreshes the embeddings
    """
    embeddings = Embeddings()
    embeddings.generate_and_save_embeddings()
    return {"message": "Embeddings refreshed!"}


@router.get("/ask")
async def ask_gpt(question: str) -> dict[str, str]:
    """
    Returns an answer to a question about the GitHub API
    """
    if not question:
        raise HTTPException(status_code=400, detail="Question is empty")

    assistant = GithubApiAssistant()
    response = assistant.ask(question)
    return {"response": response}
