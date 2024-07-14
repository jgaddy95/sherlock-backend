from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from ..services.llm_service import scan_project
from ..services.file_service import get_project_files
from ..services.project_scanner import process_project  


scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/api/scan', methods=['POST'])
def scan_project_route():
    data = request.json
    project_id = data.get('project_id')
    
    if not project_id:
        return jsonify({"error": "No project ID provided"}), 400
    
    project_files = get_project_files(project_id)
    if not project_files:
        return jsonify({"error": "Project not found or empty"}), 404
    
    scan_results = scan_project(project_files)
    return jsonify({"scan_results": scan_results}), 200


@scan_bp.route('/api/scan-project', methods=['POST'])
@cross_origin()
def scan_project_detailed():
    data = request.json
    project_id = data.get('project_id')
    
    if not project_id:
        return jsonify({"error": "No project ID provided"}), 400

    try:
        formatted_content = process_project(project_id)
        return jsonify({
            "success": True, 
            "formatted_content": formatted_content,
            "content_preview": formatted_content[:2000],  # Return first 2000 characters as preview
            "content_length": len(formatted_content),
            "project_id": project_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500