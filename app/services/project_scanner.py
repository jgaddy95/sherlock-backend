import os
import json
from flask import current_app

def get_directory_structure(project_path):
    project_structure = {}
    file_contents = {}
    file_references = {}

    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, project_path)
            
            # Use only the file name as the key, not the full path
            file_name = os.path.basename(relative_path)
            
            # Read file contents
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents[file_name] = content
                    
                    # Initialize file references
                    file_references[file_name] = []
                    
                    # Simple reference detection
                    for other_file in file_contents.keys():
                        if other_file != file_name and other_file in content:
                            file_references[other_file].append(file_name)
            except Exception as e:
                print(f"Error reading file {file_path}: {str(e)}")
                file_contents[file_name] = f"Error reading file: {str(e)}"
            
            # Build project structure
            project_structure[file_name] = None

    return project_structure, file_contents, file_references

def scan_project(project_path):
    project_structure, file_contents, file_references = get_directory_structure(project_path)

    # Generate formatted content
    formatted_content = "Project Overview:\n"
    formatted_content += json.dumps(project_structure, indent=2) + "\n\n"

    formatted_content += "File References:\n"
    for file, references in file_references.items():
        formatted_content += f"{file} is referenced in: {', '.join(references)}\n"
    formatted_content += "\n"

    for file_name, content in file_contents.items():
        formatted_content += f"*This is the code for {file_name}*\n\n"
        formatted_content += content + "\n\n"
        formatted_content += f"*This is the end of {file_name}*\n\n"

    return formatted_content

def process_project(project_id):
    project_path = os.path.join(current_app.config['UPLOAD_FOLDER'], project_id)
    return scan_project(project_path)