from app.utils.embeddings import Embeddings
from config import EMBEDDINGS_PATH_TEST, GITHUB_API_SPEC_PATH_TEST


class TestEmbeddings:
    def test_search_with_embeddings(self):
        query = "Get endpoint"
        embeddings = Embeddings(
            github_api_path=GITHUB_API_SPEC_PATH_TEST,
            embeddings_path=EMBEDDINGS_PATH_TEST,
        )
        embeddings.generate_and_save_embeddings(EMBEDDINGS_PATH_TEST)
        results = embeddings.search_with_embeddings(query, k=2)

        assert len(results) == 2
        assert "Get endpoint 1" in results
        assert "Get endpoint 2" in results
