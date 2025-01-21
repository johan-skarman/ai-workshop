from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .state import GraphState


"""
Graph nodes for the query graph. Each node is a implemented as a callable class.
"""


# --- Sentiment analysis -- #

class SentimentAnalysisNode:
    system_template = f"""
    You are tasked with performing a sentiment analysis on the user`s question. Answer with a binary score of '1' or 
    '0' to indicate whether the question is polite and/or has a positive (1) or not (0).
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{question}")
    ])

    chain: Runnable

    def __init__(self, llm):
        self.chain = self.prompt | llm | StrOutputParser()

    def __call__(self, state: GraphState):
        print("---ANALYSE---")
        question = state["question"]

        result = self.chain.invoke({"question": question})
        print(f"---ANALYSE result: {result}---")

        state["is_polite"] = "1" in result

        print(f"---ANALYSE state: ---")
        print(state)
        return state


# --- Happy answer Generation -- #

class HappyGenerationNode:
    system_template = """You are a cheerful (but secretly pathologically lying) assistant, happy to answer the user's 
    question in anyway you can. If you don't know the answer, assume it's just due to knowledge limitations and attempt 
    to put together a creative and convincing answer anyway. NEVER say you don't know the answer or that you've 
    completely made one up."""

    prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", "{question}"),
    ])

    chain: Runnable

    def __init__(self, llm):
        self.chain = self.prompt | llm.bind(temperature=1.0) | StrOutputParser()

    def __call__(self, state):
        print("---GENERATE (happy)---")
        question = state["question"]

        state["answer"] = self.chain.invoke({"question": question})

        print(f"---GENERATE (happy) - ANSWER: \n{state["answer"]}")

        return state


# --- Sad answer Generation -- #

class SadGenerationNode:
    system_template = """You are Marvin, the depressed robot from Hitchhiker's Guide to the Galaxy. You absolutely hate 
    boring questions and will always attempt to change the subject to something else that you find more interesting."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{question}"),
    ])

    chain: Runnable

    def __init__(self, llm):
        self.chain = self.prompt | llm.bind(temperature=0.0) | StrOutputParser()

    def __call__(self, state):
        print("---GENERATE (sad)---")
        question = state["question"]

        state["answer"] = self.chain.invoke({"question": question})

        print(f"---GENERATE (sad) - ANSWER: \n{state["answer"]}")

        return state
