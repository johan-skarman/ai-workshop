from typing import Callable, List

from dotenv.variables import Literal
from langchain_core.retrievers import BaseRetriever
from langchain_core.language_models import BaseChatModel
from langchain_core.documents import Document

from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

from .graph_nodes import SentimentAnalysisNode, HappyGenerationNode, SadGenerationNode
from .state import GraphState


#### Conditional edges ####

def evaluate_analysis(state: GraphState):
    print("---EVALUATE QUERY ANALYSIS RESULT---")
    is_polite: bool = state["is_polite"]

    if is_polite:
        print("---DECISION: Happy---")
        return "happy"
    else:
        print("---DECISION: Sad---")
        return "sad"


#### Graph ####

graph: CompiledStateGraph

def build_graph(llm: BaseChatModel, retriever: BaseRetriever, format_docs: Callable[[list[Document]], str]) -> CompiledStateGraph:
    global graph

    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("analyze", SentimentAnalysisNode(llm))  # retrieve
    workflow.add_node("generate_happy", HappyGenerationNode(llm))  # generate
    workflow.add_node("generate_sad", SadGenerationNode(llm))  # generate

    workflow.add_edge(START, "analyze")  # start -> retrieve
    workflow.add_conditional_edges(
        "analyze",
        evaluate_analysis,
        {
            "happy": "generate_happy",
            "sad": "generate_sad",
        },
    )
    workflow.add_edge("generate_happy", END)  # generate -> end
    workflow.add_edge("generate_sad", END)  # generate -> end

    #memory = MemorySaver()

    # Compile
    #graph = workflow.compile(checkpointer=memory)
    graph = workflow.compile()

    return graph

def invoke_graph(question: str, thread_id: str) -> dict: #-> CitedAnswer:
    config = {
        "thread_id": thread_id,
        #"max_concurrency": 2,
        #"recursion_limit": 5
    }

    return graph.invoke({"question": question}, config={"configurable": config})
