from fastapi import FastAPI
from app.github_api.fetch import save_github_api

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/refresh-github-api")
async def refresh_github_api_file():
    save_github_api()
    return {"message": "GitHub API refreshed!"}
