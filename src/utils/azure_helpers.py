from azure.storage.blob import BlobServiceClient

from configs import settings


def upload_file_azure(local_path: str, request_id: str) -> str:
    # todo: add exception handling
    blob_client = BlobServiceClient.from_connection_string(
        conn_str=settings.azure_storage_connection_string
    )
    container = blob_client.get_container_client(
        container=settings.azure_storage_container_name
    )
    blob = container.get_blob_client(f"{request_id}.mp4")
    with open(local_path, "rb") as file:
        blob.upload_blob(data=file, overwrite=True)
        return blob.url
