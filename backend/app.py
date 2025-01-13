# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from annotation_types.scoring import ScoringAnnotation
from database.db_utils import init_db
from config import SERVER, CORS_ORIGINS

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": CORS_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})


init_db()

annotation_handler = ScoringAnnotation()

@app.route("/api/annotation/next", methods=["GET"])
def get_next_annotation():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"error": "Username required"}), 400

    data = annotation_handler.get_next_data(username)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({"message": "No more data"}), 200

@app.route("/api/annotation/submit", methods=["POST"])
def submit_annotation():
    payload = request.json
    if not payload:
        return jsonify({"error": "Missing payload"}), 400

    data_id = payload.get("dataId")
    username = payload.get("userName", "").strip()
    score = payload.get("score")

    if not data_id or not username or score is None:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        annotation_handler.submit_annotation(data_id, username, score)
        return jsonify({"message": "Annotation submitted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/annotation/progress", methods=["GET"])
def get_progress():
    username = request.args.get("username", "").strip()
    if not username:
        return jsonify({"error": "Username required"}), 400

    try:
        progress = annotation_handler.get_progress(username)
        return jsonify(progress), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(
        host=SERVER['host'],
        port=SERVER['port'],
        debug=SERVER['debug']
    )
