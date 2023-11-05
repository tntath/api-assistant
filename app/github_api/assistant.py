import os

import openai

from app.utils.embeddings import Embeddings

openai.api_key = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-3.5-turbo"


class GithubApiAssistant:
    def __init__(self):
        self.embeddings = Embeddings()

    def ask(self, query) -> str:
        results = self.embeddings.search_with_embeddings(query)

        results_str = "\n".join(results)

        question = f"Based on the following information from the GitHub API spec:\n{results_str}\nAnswer the following question regarding the GitHub API:\n{query}\nIf the question is not relevant or you cannot provide an answer, gracefully indicate it. Also, if the question is out of context, ask gracefully the user to provide you with a relevant question."

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. You are helping a programmer understand the GitHub API.",
                },
                {"role": "user", "content": question},
            ],
        )

        return completion.choices[0].message.content
