import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import uuid

upload_bp = Blueprint('upload', __name__)

def get_directory_structure(path):
    """
    Generate a nested dictionary that represents the folder structure of rootdir
    """
    structure = {}
    for root, dirs, files in os.walk(path):
        current = structure
        path_parts = root[len(path):].split(os.sep)
        for part in path_parts:
            if part:
                current = current.setdefault(part, {})
        for file in files:
            current[file] = None
    return structure

def dict_to_tree(d, name):
    """
    Convert the dictionary to the desired tree structure
    """
    if d is None:
        return {"name": name, "type": "file"}
    return {
        "name": name,
        "type": "directory",
        "children": [dict_to_tree(v, k) for k, v in d.items()]
    }

@upload_bp.route('/api/upload', methods=['POST'])
def upload_project():
    if 'project' not in request.files:
        return jsonify({"error": "No project part"}), 400
    
    files = request.files.getlist('project')
    
    project_id = str(uuid.uuid4())
    project_path = os.path.join(current_app.config['UPLOAD_FOLDER'], project_id)
    os.makedirs(project_path, exist_ok=True)
    
    file_count = 0
    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(project_path, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            file_count += 1
    
    dir_structure = get_directory_structure(project_path)
    root_name = next(iter(dir_structure)) if dir_structure else "Unnamed Project"
    tree = dict_to_tree(dir_structure, root_name)
    
    return jsonify({
        "project_id": project_id,
        "file_count": file_count,
        "structure": tree
    }), 200