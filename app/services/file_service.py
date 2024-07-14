import os
import uuid
from werkzeug.utils import secure_filename
import logging

UPLOAD_FOLDER = 'uploads'

def save_uploaded_files(files):
    project_id = str(uuid.uuid4())
    project_path = os.path.join(UPLOAD_FOLDER, project_id)
    os.makedirs(project_path, exist_ok=True)
    logging.info(f"Created project directory: {project_path}")

    saved_files = []
    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(project_path, filename)
            file.save(file_path)
            saved_files.append(filename)
            logging.info(f"Saved file: {file_path}")

    return {
        "project_id": project_id,
        "file_count": len(saved_files),
        "files": saved_files
    }

def get_project_files(project_id):
    project_path = os.path.join(UPLOAD_FOLDER, project_id)
    if not os.path.exists(project_path):
        return None
    
    project_files = []
    for filename in os.listdir(project_path):
        file_path = os.path.join(project_path, filename)
        with open(file_path, 'r') as file:
            content = file.read()
        project_files.append({"name": filename, "content": content})
    
    return project_files