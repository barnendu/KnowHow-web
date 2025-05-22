import os
from app.chat.embeddings.openai import embeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore


vector_store = PineconeVectorStore(
    index_name=os.getenv("PINECONE_INDEX_NAME"),
    embedding=embeddings,
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)


def build_retriever(chat_args):
    search_kwargs = {"filter": {"doc_id": {'$in': chat_args.document_id }}}
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
