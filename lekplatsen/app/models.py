from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama

from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureOpenAIEmbeddings

#from langchain_openai import ChatOpenAI
#from langchain_anthropic import ChatAnthropic
#from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

def load_llm() -> BaseChatModel:
    # Azure OpenAI
    from langchain_openai import AzureChatOpenAI
    api_version = "2024-10-01-preview"
    llm = AzureChatOpenAI(deployment_name="gpt-4o-mini", temperature=0.0, openai_api_version=api_version)

    # OpenAI
    #from langchain_openai import ChatOpenAI


    # For using for local LLM served via OpenAI compatible API (for instance LM Studio, Ollama etc)
    # llm = ChatOpenAI(
    #     #base_url="http://localhost:11434/v1", # Ollama
    #     base_url="http://localhost:1234/v1", # LM Studio
    #     openai_api_key="ollama",
    #     model_name="qwen2.5:14b",  # For Ollama
    #     temperature=0.1,
    # )


    # Ollama
    #llm = ChatOllama(model="qwen2.5", temperature=0.1)


    # Anthropic (Claude)
    # llm = ChatAnthropic(
    #     model='claude-3-opus-20240229',
    #     temperature=0.0,
    # )


    # Models from HuggingFace
    # See https://python.langchain.com/docs/integrations/chat/huggingface/
    # from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
    # llm_pipeline = HuggingFacePipeline.from_model_id(
    #     model_id="microsoft/Phi-3.5-mini-instruct",
    #     task="text-generation",
    #     # See https://huggingface.co/docs/transformers/v4.46.3/en/main_classes/text_generation#transformers.GenerationConfig
    #     pipeline_kwargs=dict(
    #         max_new_tokens=64,
    #         return_full_text=False, # Don't return prompts in response
    #     ),
    # )
    # llm = ChatHuggingFace(llm=llm_pipeline)

    print(f"Initialized LLM ({llm})")
    return llm

# See https://huggingface.co/spaces/mteb/leaderboard
# hf_embeddings_model="intfloat/multilingual-e5-large-instruct" # 560M params, 2.09GB mem use, 1024 dim, 514 tokens, 63.61 avg score
# # hf_embeddings_model="avsolatorio/GIST-all-MiniLM-L6-v2" # 23M params, 0.08GB mem use, 384 dim, 512 tokens, 59 avg score
# # hf_embeddings_model="Salesforce/SFR-Embedding-2_R" # 7B params, 26GB mem use, 4096 dim, 32k tokens, 70.32 avg score
# # hf_embeddings_model="nvidia/NV-Embed-v2" # 7B params, 29GB mem use, 4096 dim, 32k tokens, 72.31 avg score
# def load_huggingface_embeddings(hf_embeddings_model="intfloat/multilingual-e5-large-instruct") -> Embeddings:
#     embeddings = HuggingFaceEmbeddings(model_name=hf_embeddings_model)
#     print(f"Using HuggingFace model: {hf_embeddings_model}")
#     return embeddings

def load_azure_open_ai_embeddings(openai_embeddings_model: str = "text-embedding-3-large", dimensions:int=None) -> Embeddings:
    embeddings = AzureOpenAIEmbeddings(model=openai_embeddings_model, dimensions=dimensions)
    print(f"Using OpenAI model: {openai_embeddings_model}")
    return embeddings
