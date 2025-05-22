from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.chat.vector_stores.pinecone import vector_store

def create_emdeddings(document_id:str, file_path:str, file_extension:str):
    
    if file_extension == "pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension == "txt":
        loader = TextLoader(file_path)
    elif file_extension == "docx":
        loader = Docx2txtLoader(file_path)
    elif file_extension == "csv":
        loader = CSVLoader(file_path)
    else:
        raise ValueError("Invalid file extension")
    
    if file_extension == "csv":
        docs = loader.load()
    else:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = loader.load_and_split(text_splitter)
    for doc in docs:
        doc.metadata = {
            "text": doc.page_content,
            "doc_id": document_id
        }
    vector_store.add_documents(docs)