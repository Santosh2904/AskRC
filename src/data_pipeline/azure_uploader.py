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