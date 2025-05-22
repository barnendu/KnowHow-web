from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import  TextLoader
from app.chat.vector_stores.pinecone import vector_store
from app.chat.embeddings.openai import embeddings

def audio_embeddings(file_path, document_id):
    loader = TextLoader(file_path)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = loader.load_and_split(text_splitter)
    for doc in docs:
        doc.metadata = {
            "text": doc.page_content,
            "doc_id": document_id
        }
    vector_store.add_documents(docs)