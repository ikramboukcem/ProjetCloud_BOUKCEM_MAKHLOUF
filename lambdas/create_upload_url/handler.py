import boto3
import os
import json
import uuid


def lambda_handler(event, context):
    """
    Lambda qui génère une URL pré-signée pour uploader un fichier
    dans le bucket S3/MinIO.
    """

    # Nom du bucket : variable d'environnement fournie par OpenTofu
    bucket_name = os.environ.get("BUCKET_NAME", "docdrop-documents-meriem-makhfouf")

    # Connexion à MinIO (local)
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",    
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )

    # Nom de fichier envoyé par le frontend
    body = event or {}
    file_name = body.get("fileName")

    if not file_name:
        # si rien n'est fourni, on génère un nom unique
        file_name = f"{uuid.uuid4()}.bin"

    # Chemin réel dans le bucket
    object_key = f"uploads/{file_name}"

    # Générer l'URL pour uploader le fichier
    upload_url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_key,
        },
        ExpiresIn=3600,  # expire dans 1 heure
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "documentId": object_key,
            "uploadUrl": upload_url,
        }),
    }


# Test local possible
if __name__ == "__main__":
    print(lambda_handler({"fileName": "test-local.txt"}, None))
