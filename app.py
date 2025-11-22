from flask import Flask, request, jsonify
from lambdas.create_upload_url.handler import lambda_handler
import json

app = Flask(__name__)


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

from urllib.parse import urlparse
# ... le reste de tes imports en haut

@app.route("/upload-url", methods=["GET"])
def generate_upload_url_from_query():
    """
    Version GET /upload-url?url=...
    utilisée par le frontend actuel (uploadFromUrl()).
    On récupère l'URL, on en déduit un nom de fichier, puis
    on appelle la Lambda create_upload_url comme avant.
    """
    file_url = request.args.get("url")

    if not file_url:
        return jsonify({"error": "url parameter is required"}), 400

    # Essayer d'extraire un nom de fichier à partir de l'URL
    try:
        parsed = urlparse(file_url)
        path = parsed.path
        file_name = path.split("/")[-1] or "document-from-url"
    except Exception:
        # Si jamais ça foire, on prend une valeur par défaut
        file_name = "document-from-url"

    lambda_result = lambda_handler({"fileName": file_name}, None)
    body = json.loads(lambda_result["body"])
    status_code = lambda_result.get("statusCode", 200)

    return jsonify(body), status_code


if __name__ == "__main__":
    # L'API sera disponible sur http://localhost:5000
    app.run(port=5000, debug=True)

