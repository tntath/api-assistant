import json
import os

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import EBEDDINGS_PATH, GITHUB_API_SPEC_PATH

model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")


class Embeddings:
    def __init__(self):
        with open(GITHUB_API_SPEC_PATH, "r") as file:
            api_spec = json.load(file)

        self.api_texts = [
            endpoint_info["description"]
            for _, endpoint_data in api_spec["paths"].items()
            for _, endpoint_info in endpoint_data.items()
        ]

        if not os.path.exists(EBEDDINGS_PATH):
            self.generate_and_save_embeddings()

        self.api_embeddings = self.load_embeddings()

    def generate_and_save_embeddings(self) -> None:
        api_embeddings = model.encode(self.api_texts)
        np.save(EBEDDINGS_PATH, api_embeddings)

    def load_embeddings(self) -> np.ndarray:
        return np.load(EBEDDINGS_PATH)

    def search_with_embeddings(self, query: str, k: int = 10) -> list[str]:
        api_embeddings = self.api_embeddings
        index = faiss.IndexFlatL2(api_embeddings.shape[1])
        index.add(api_embeddings)

        query_embedding = model.encode([query])
        _, indices = index.search(query_embedding, k)

        results = [self.api_texts[i] for i in indices[0]]
        return results
