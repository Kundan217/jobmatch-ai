import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityService:
    def __init__(self) -> None:
        self._model = None
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            self._model = None

    def score(self, resume_text: str, job_description: str) -> int:
        if self._model:
            embeddings = self._model.encode([resume_text, job_description])
            value = self._cosine(embeddings[0], embeddings[1])
        else:
            vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            matrix = vectorizer.fit_transform([resume_text, job_description])
            value = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        return max(0, min(100, round(value * 100)))

    @staticmethod
    def _cosine(a: np.ndarray, b: np.ndarray) -> float:
        denominator = np.linalg.norm(a) * np.linalg.norm(b)
        if denominator == 0:
            return 0.0
        return float(np.dot(a, b) / denominator)


similarity_service = SimilarityService()
