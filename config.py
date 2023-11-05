import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
GITHUB_API_SPEC_PATH = os.path.join(DATA_DIR, "github_api_spec.json")
EBEDDINGS_PATH = os.path.join(DATA_DIR, "github_api_embeddings.npy")
