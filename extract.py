import io
from azure.storage.blob import BlobServiceClient
import zipfile

connectionString = ""  # <- Connection String of container

# Download
inputcontainerName = "01-raw"
inputBlob = "archive"

# Upload
outputcontainerName = "02-extracted"
outputSalesBlob = "Sales.csv"
outputProductBlob = "products.csv"

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connectionString)

# Download the zip file
blob_client = blob_service_client.get_blob_client(container=inputcontainerName, blob=inputBlob)
blob_data = blob_client.download_blob().readall()

# io.BytesIO to convert the bytes into a file-like object
with zipfile.ZipFile(io.BytesIO(blob_data), 'r') as zip_ref:
    zip_ref.extractall("archive")

# Upload extracted files
blob_client = blob_service_client.get_blob_client(container=outputcontainerName, blob=outputSalesBlob)
with open(f"archive/{outputSalesBlob}", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

blob_client = blob_service_client.get_blob_client(container=outputcontainerName, blob=outputProductBlob)
with open(f"archive/{outputProductBlob}", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)
