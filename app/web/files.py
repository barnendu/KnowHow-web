import os
import requests
import tempfile
from flask import g, current_app
from azure.storage.blob import BlobServiceClient
from app.web.config import Config
from app.web.db.models import Document

connection_string = f"DefaultEndpointsProtocol=https;AccountName={Config.ACCOUNT_NAME};AccountKey={Config.ACCOUNT_KEY};EndpointSuffix=core.windows.net"


def upload(local_file_path, file_name):

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    if g.user is None:
        return {"message":"Unauthorized"}, 401
    user_name = g.user.id

    folder_name = f"{user_name}/{file_name}"
    blob_client = blob_service_client.get_blob_client(container=Config.CONTAINER_NAME, blob=folder_name)
    with open(local_file_path, "rb") as f:
        blob_client.upload_blob(f)
        return {"message":"File uploaded successfully!"}, 200
    
def create_download_url(file_id):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    doc = Document.find_by(id=file_id).as_dict()
    url = []
    blob_client = blob_service_client.get_blob_client(container=Config.CONTAINER_NAME, blob=f"{g.user.id}/{doc["name"]}")
    url.append(blob_client.url)
    if doc["document_ext"] == "wav" or doc["document_ext"] == "mp3":
        blob_client = blob_service_client.get_blob_client(container=Config.CONTAINER_NAME, blob=f"{g.user.id}/{doc["name"].split(".")[0]}.txt")
        url.append(blob_client.url)
    return url

def download(file_id):
    return _Download(file_id)



class _Download:
    def __init__(self, file_id):
        self.file_id = file_id
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = ""

    def download(self):
        self.file_path = os.path.join(self.temp_dir.name, self.file_id)
        download_url = create_download_url(self.file_id)[0];
        print(download_url)
        response = requests.get(download_url, stream=True)
        with open(self.file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return self.file_path

    def cleanup(self):
        self.temp_dir.cleanup()

    def __enter__(self):
        return self.download()

    def __exit__(self, exc, value, tb):
        self.cleanup()
        return False
    

