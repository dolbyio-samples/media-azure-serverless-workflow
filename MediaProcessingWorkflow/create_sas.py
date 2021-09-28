#Functions to create Azure Blob SAS URLs

from datetime import datetime, timedelta
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, ContainerSasPermissions, generate_container_sas

def create_azure_blob_sas(AZURE_ACC_NAME,AZURE_CONTAINER,AZURE_BLOB_INPUT,AZURE_PRIMARY_KEY,AZURE_BLOB_OUTPUT_SUFFIX):
    """
    Creates a blob SAS for file access.
    Inputs:
       AZURE_ACC_NAME: Storage account name.
       AZURE_CONTAINER: Container name.
       AZURE_BLOB_INPUT: Blob name.
       AZURE_PRIMARY_KEY: Azure storage account key.
       AZURE_BLOB_OUTPUT_SUFFIX: The suffix added to the output file, for example "_enhanced" or "_cleaned".
    Returns: 
       input_sas: The SAS URL to the input blob.
       output_sas: The SAS URL to the output blob.
    """
    if AZURE_BLOB_INPUT == None: AZURE_BLOB_INPUT = "file"

    #Creates the input and output SAS URLs
    AZURE_BLOB_OUTPUT = AZURE_BLOB_INPUT.split(".")[0] + AZURE_BLOB_OUTPUT_SUFFIX

    input_sas_blob = generate_blob_sas(account_name=AZURE_ACC_NAME, 
                                    container_name=AZURE_CONTAINER,
                                    blob_name=AZURE_BLOB_INPUT,
                                    account_key=AZURE_PRIMARY_KEY,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.utcnow() + timedelta(hours=5))

    output_sas_blob = generate_blob_sas(account_name=AZURE_ACC_NAME, 
                                    container_name=AZURE_CONTAINER,
                                    blob_name=AZURE_BLOB_OUTPUT,
                                    account_key=AZURE_PRIMARY_KEY,
                                    permission=BlobSasPermissions(read=True, write=True, create=True),
                                    expiry=datetime.utcnow() + timedelta(hours=5))

    input_sas = 'https://'+AZURE_ACC_NAME+'.blob.core.windows.net/'+AZURE_CONTAINER+'/'+AZURE_BLOB_INPUT+'?'+input_sas_blob
    output_sas = 'https://'+AZURE_ACC_NAME+'.blob.core.windows.net/'+AZURE_CONTAINER+'/'+AZURE_BLOB_OUTPUT+'?'+output_sas_blob

    return input_sas,output_sas

def create_container_sas(AZURE_ACC_NAME,AZURE_CONTAINER,AZURE_PRIMARY_KEY):
    """
    Creates the an output SAS URL for the specified container.
    Inputs:
       AZURE_ACC_NAME: Storage account name.
       AZURE_CONTAINER: Container name.
       AZURE_PRIMARY_KEY: Azure storage account key.
    Returns: 
       output_sas: The SAS URL to the output container.
    """

    output_sas_blob = generate_container_sas(account_name=AZURE_ACC_NAME, 
                                    container_name=AZURE_CONTAINER,
                                    account_key=AZURE_PRIMARY_KEY,
                                    permission=ContainerSasPermissions(read=True, write=True, list=True, delete=True),
                                    expiry=datetime.utcnow() + timedelta(hours=5))
    output_sas = 'https://'+AZURE_ACC_NAME+'.blob.core.windows.net/'+AZURE_CONTAINER+'?'+output_sas_blob
    return output_sas

