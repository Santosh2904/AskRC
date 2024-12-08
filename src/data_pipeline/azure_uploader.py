"""
azure_uploader.py

This module uploads preprocessed data to Azure Blob Storage. 
It provides a function to upload files to a specified container in Azure Blob Storage.
"""
import os
from dotenv import load_dotenv
import datetime
from config.mlflow_config import *
collector = MetricsCollector()

load_dotenv()

from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient


client_id = os.getenv('AZURE_CLIENT_ID')
client_secret_value = os.getenv('AZURE_CLIENT_SECRET_VALUE')
tenant_id = os.getenv('AZURE_TENANT_ID')
storage_account_url = os.getenv('AZURE_BLOB_STORAGE_URL')

container_name = "preprocessed-data"
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret_value,
    tenant_id=tenant_id
)


# def download_from_blob_storage():
#     blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=credentials)
#     container_client = blob_service_client.get_container_client(container=container_name)
#     file_content = container_client.get_blob_client(blob=blob_name).download_blob().readall().decode("utf-8")

def upload_to_blob(file_path, file_name):
    """
    Upload a file to Azure Blob Storage.
    
    Args:
        file_path (str): The path of the file to upload.
    """
    
    blob_version = datetime.datetime.now().strftime("%d%m%yT%H%M%S")
    collector.add_metric('blob_version',blob_version)
    container_client = getContainerClient(container_name)
    # Open the file and read its content
    try:
        with open(file_path, 'r') as file:
            container_client.upload_blob(name = file_name, data=file.read(), overwrite=True)
            print(file_path + " has been uploaded to blob storage")
    except FileNotFoundError:
        print("The file was not found at the specified path.")

def getBlobServiceClient():
    return BlobServiceClient(account_url=storage_account_url, credential=credentials)

def getContainerClient(container_name):
    blob_service_client = getBlobServiceClient()
    return blob_service_client.get_container_client(container=container_name)