import os
from .llm_service import analyze_code

UPLOAD_FOLDER = 'uploads'

def scan_project(project_id):
    project_path = os.path.join(UPLOAD_FOLDER, project_id)
    if not os.path.exists(project_path):
        return {"error": "Project not found"}

    scan_results = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
                analysis = analyze_code(content)
                scan_results.append({
                    "file": file,
                    "analysis": analysis
                })

    return {"scan_results": scan_results}