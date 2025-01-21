from typing import List, TypedDict

from langchain_core.documents import Document
from langgraph.graph import MessagesState


#### Graph state ####

#class GraphState(MessagesState):
class GraphState(TypedDict):
    question: str
    is_polite: bool
    answer: str
