from azure.storage.blob import BlobServiceClient
from app.web.config import Config
from flask import g, current_app
import os


connection_string = f"DefaultEndpointsProtocol=https;AccountName={Config.ACCOUNT_NAME};AccountKey={Config.ACCOUNT_KEY};EndpointSuffix=core.windows.net"

# NOTE: This function designed to save the transcript along with audio file in blob storage:
def sent_transcript_to_blob_storage(local_file_path):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        if g.user is None:
            return {"message":"Unauthorized"}, 401
        user_name = g.user.id
        # NOTE: Creating the Bolb path with the combination of user_id and file names:
        folder_name = f"{user_name}/{local_file_path.split("/")[1]}"
        blob_client = blob_service_client.get_blob_client(container=Config.CONTAINER_NAME, blob=folder_name)
        with open(local_file_path, "rb") as f:
            blob_client.upload_blob(f)
            # Remove the file after uploading to blob storage:
            os.remove(local_file_path)
            print(f"File '{local_file_path}' deleted successfully.")
    except Exception as e:
        print(f"Error: {e}")