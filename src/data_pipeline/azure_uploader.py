"""
azure_uploader.py

This module uploads preprocessed data to Azure Blob Storage. 
It provides a function to upload files to a specified container in Azure Blob Storage.
"""

from azure.storage.blob import BlobServiceClient

def upload_to_blob(file_path, container_name, connection_string):
    """
    Upload a file to Azure Blob Storage.
    
    Args:
        file_path (str): The path of the file to upload.
        container_name (str): The name of the Azure Blob container.
        connection_string (str): The Azure Blob Storage connection string.
    """
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)
    
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {file_path} to Azure Blob Storage")
