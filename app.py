from flask import Flask, request, jsonify
from flask_cors import CORS
from lambdas.create_upload_url.handler import lambda_handler
from urllib.parse import urlparse
import json
import requests


app = Flask(__name__)
CORS(app)   # ← Active les CORS pour toutes les routes


@app.route("/upload-url", methods=["POST"])
def generate_upload_url():
    """
    Endpoint d'API qui appelle la Lambda create_upload_url
    et retourne une URL pré-signée pour uploader un document.
    """

    data = request.get_json()

    if not data or "fileName" not in data:
        return jsonify({"error": "fileName is required"}), 400

    file_name = data["fileName"]

    # Appel de ta Lambda Python existante
    lambda_result = lambda_handler({"fileName": file_name}, None)

    # lambda_result["body"] est une chaîne JSON → on la reconvertit en dict
    body = json.loads(lambda_result["body"])
    status_code = lambda_result.get("statusCode", 200)

    return jsonify(body), status_code



@app.route("/upload-url", methods=["GET"])
def upload_from_url():
    """
    Version GET /upload-url?url=...
    - récupère l'URL du fichier
    - demande à la Lambda une URL pré-signée
    - télécharge le fichier
    - l'envoie vers MinIO via l'URL pré-signée
    - renvoie au front l'ID du document
    """

    file_url = request.args.get("url")
    if not file_url:
        return jsonify({"error": "url parameter is required"}), 400

    # 1) Essayer d'extraire un nom de fichier à partir de l'URL
    try:
        parsed = urlparse(file_url)
        path = parsed.path
        file_name = path.split("/")[-1] or "document-from-url"
    except Exception:
        file_name = "document-from-url"

    # 2) Appel de la Lambda pour obtenir l'uploadUrl + documentId
    lambda_result = lambda_handler({"fileName": file_name}, None)
    body = json.loads(lambda_result["body"])
    status_code = lambda_result.get("statusCode", 200)

    if status_code != 200 or "uploadUrl" not in body:
        return jsonify({"error": "Unable to get upload URL"}), 500

    upload_url = body["uploadUrl"]
    document_id = body["documentId"]

    # 3) Télécharger le fichier à partir de file_url
    try:
        resp = requests.get(file_url, stream=True)
        if not resp.ok:
            return jsonify({"error": f"Failed to download file: {resp.status_code}"}), 400
    except Exception as e:
        return jsonify({"error": f"Exception while downloading file: {str(e)}"}), 500

    # 4) Envoyer les bytes vers MinIO en utilisant l'URL pré-signée
    try:
        put_resp = requests.put(upload_url, data=resp.content)
        if not put_resp.ok:
            return jsonify({"error": f"Failed to upload to storage: {put_resp.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": f"Exception while uploading to storage: {str(e)}"}), 500

    # 5) Tout s'est bien passé -> on renvoie l'ID au front
    return jsonify({
        "documentId": document_id,
        "status": "uploaded"
    }), 200


if __name__ == "__main__":
    # L'API sera disponible sur http://localhost:5000
    app.run(port=5000, debug=True)

