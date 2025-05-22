from langchain_openai import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain


def build_chat(chat_args: ChatArgs):
    retriever = build_retriever(chat_args)
    llm = build_llm(chat_args)
    condense_question_llm = ChatOpenAI()
    memory = build_memory(chat_args.conversation_id)
    return StreamingConversationalRetrievalChain.from_llm(
        llm,
        retriever,
        condense_question_llm=condense_question_llm,
        memory=memory,
        verbose=True
    )
