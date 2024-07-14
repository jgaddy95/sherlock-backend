import os
from flask import Blueprint, jsonify, current_app

file_bp = Blueprint('file', __name__)

@file_bp.route('/api/file/<project_id>/<path:file_path>', methods=['GET'])
def get_file_content(project_id, file_path):
    project_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], project_id)
    file_full_path = os.path.join(project_folder, file_path)
    
    if not os.path.exists(file_full_path) or not os.path.isfile(file_full_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        with open(file_full_path, 'r') as file:
            content = file.read()
        return jsonify({"content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500