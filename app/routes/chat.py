from flask import Blueprint, request, jsonify
from ..services.llm_service import chat_with_gpt4

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages')
    scanned_project_content = data.get('scannedProjectContent')
    
    print("Received messages:", messages)
    print("Scanned project content (first 500 chars):", scanned_project_content[:500] if scanned_project_content else None)
    
    if not messages:
        return jsonify({"error": "Messages are required"}), 400
    
    # Here, you should pass the scanned_project_content to your LLM service
    response = chat_with_gpt4(messages, scanned_project_content)
    
    return response