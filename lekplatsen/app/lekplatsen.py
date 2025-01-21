from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

from .datasources.vector_store import VectorStore
from .datasources.chroma_pdf import ChromaPDFVectorStore
from .query.graph import build_graph, invoke_graph
from .models import load_llm

_ = load_dotenv(find_dotenv())

vector_store: VectorStore

@asynccontextmanager
async def lifespan(app: FastAPI):
    llm = load_llm()
    global vector_store
    vector_store = ChromaPDFVectorStore()
    build_graph(llm=llm, retriever=vector_store.retriever, format_docs=vector_store.format_docs)
    yield


api = FastAPI(lifespan=lifespan)


class UserQuestion(BaseModel):
    question: str


# Chat endpoint
@api.post("/chat/{thread_id}")
async def chat(thread_id: str, question: UserQuestion):
    answer = invoke_graph(question=question.question, thread_id=thread_id)

    print(f"-----> Answer: \n{answer}")

    return answer


@api.get("/ingest")
async def chat():
    doc_count = vector_store.ingest()

    return f"Ingested {doc_count} documents (splits)"
