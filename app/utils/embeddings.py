import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDINGS_PATH, GITHUB_API_SPEC_PATH

model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")


class Embeddings:
    def __init__(
        self, github_api_path=GITHUB_API_SPEC_PATH, embeddings_path=EMBEDDINGS_PATH
    ):
        with open(github_api_path, "r") as file:
            api_spec = json.load(file)

        self.api_texts = [
            endpoint_info["description"]
            for _, endpoint_data in api_spec["paths"].items()
            for _, endpoint_info in endpoint_data.items()
        ]

        if not os.path.exists(embeddings_path):
            self.generate_and_save_embeddings(embeddings_path)

        self.api_embeddings = self.load_embeddings(embeddings_path)

    def generate_and_save_embeddings(self, embeddings_path) -> None:
        api_embeddings = model.encode(self.api_texts)
        np.save(embeddings_path, api_embeddings)

    def load_embeddings(self, embeddings_path) -> np.ndarray:
        return np.load(embeddings_path)

    def search_with_embeddings(self, query: str, k: int = 10) -> list[str]:
        api_embeddings = self.api_embeddings
        index = faiss.IndexFlatL2(api_embeddings.shape[1])
        index.add(api_embeddings)

        query_embedding = model.encode([query])
        _, indices = index.search(query_embedding, k)

        results = [self.api_texts[i] for i in indices[0]]
        return results
