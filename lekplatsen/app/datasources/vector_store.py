from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document


class VectorStore:
    embeddings: Embeddings
    retriever: BaseRetriever

    def ingest(self) -> int:
        return 0

    def format_docs(self, docs: list[Document]) -> str:
        return ''
