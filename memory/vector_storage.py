from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os

class EmbeddingProvider(ABC):
    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        pass

class VectorStorage(ABC):
    @abstractmethod
    def upsert_vector(self, memory_id: int, vector: List[float], metadata: Dict[str, Any]):
        pass

    @abstractmethod
    def search_vectors(self, workspace_id: str, query_vector: List[float], category: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_vector(self, memory_id: int):
        pass

    @abstractmethod
    def clear_workspace(self, workspace_id: str):
        pass

class LocalMockEmbeddingProvider(EmbeddingProvider):
    def get_embedding(self, text: str) -> List[float]:
        # Return a dummy vector of length 10
        return [0.1] * 10

class LocalMockVectorStorage(VectorStorage):
    def __init__(self):
        self.storage = {}

    def upsert_vector(self, memory_id: int, vector: List[float], metadata: Dict[str, Any]):
        self.storage[memory_id] = {"vector": vector, "metadata": metadata}

    def search_vectors(self, workspace_id: str, query_vector: List[float], category: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        for mem_id, data in self.storage.items():
            meta = data["metadata"]
            if meta.get("workspace_id") == str(workspace_id):
                if category and meta.get("category") != category:
                    continue
                results.append({"memory_id": mem_id, "metadata": meta, "score": 1.0})
        return results[:limit]

    def delete_vector(self, memory_id: int):
        self.storage.pop(memory_id, None)

    def clear_workspace(self, workspace_id: str):
        keys_to_delete = [
            mem_id for mem_id, data in self.storage.items()
            if data["metadata"].get("workspace_id") == str(workspace_id)
        ]
        for k in keys_to_delete:
            self.storage.pop(k)

# Provider factory based on env vars
def get_embedding_provider() -> EmbeddingProvider:
    provider = os.getenv("EMBEDDING_PROVIDER", "local")
    if provider == "local":
        return LocalMockEmbeddingProvider()
    # Add other providers like OpenAIEmbeddingProvider here
    return LocalMockEmbeddingProvider()

def get_vector_storage() -> VectorStorage:
    storage = os.getenv("VECTOR_STORAGE", "local")
    if storage == "local":
        return LocalMockVectorStorage()
    # Add other storage like PineconeVectorStorage or PgVectorStorage here
    return LocalMockVectorStorage()
