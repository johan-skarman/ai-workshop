import time

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader

from ..models import load_azure_open_ai_embeddings
from .vector_store import VectorStore


documents = [
    # URLs to PDFs
    "https://data.riksdagen.se/fil/CDA05163-DE71-448D-807D-747C997E8F3A"
]


class ChromaPDFVectorStore(VectorStore):

    embeddings: Embeddings
    vectordb: Chroma
    retriever: BaseRetriever

    def __init__(self):
        self.embeddings = load_azure_open_ai_embeddings("text-embedding-3-large", dimensions=1024)
        self.retriever = self._init_retriever()

    def _init_retriever(self) -> BaseRetriever:
        self.vectordb = Chroma(
            collection_name="pdfs",
            embedding_function=self.embeddings,
            #persist_directory=persist_directory # Optionally persist the database
        )

        return self.vectordb.as_retriever(k=3)


    def format_docs(self, docs: list[Document]) -> str:
        formatted = [
            (f"---------- Source ID: {i} ----------\n"
             f"Page number: {doc.metadata["page"]}\n"
             f"Document Snippet: \n{doc.page_content}\n")
            for i, doc in enumerate(docs)
        ]
        return f"\n\n".join(formatted)

    def ingest(self) -> int:
        splits: list[Document] = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=80
        )

        for document_url in documents:
            loader = PyPDFLoader(document_url)
            pages = loader.load()
            doc_splits = text_splitter.split_documents(pages)
            splits.extend(doc_splits)
            print(f"Loaded {document_url} - {len(doc_splits)} splits")

        batch_size = 10
        for i in range(0, len(splits), batch_size):
            batch = splits[i:i + batch_size]
            self.vectordb.add_documents(documents=batch)
            print(f"Added splits {i} to {i + batch_size}")
            time.sleep(0.25)

        return len(splits)