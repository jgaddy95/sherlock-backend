from openai import OpenAI
import anthropic
import os
from flask import Response, stream_with_context
from dotenv import load_dotenv

load_dotenv('.env')  # take environment variables from .env.

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Try to initialize OpenAI client
try:
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")

def analyze_code(code):
    if not openai_client:
        return "Error: OpenAI client not initialized. Please check your API key."
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a code analysis assistant. Identify potential bugs and suggest improvements."},
                {"role": "user", "content": f"Analyze this code:\n\n{code}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing code: {str(e)}"

def chat_with_gpt4(messages, scanned_project_content=None):
    system_message = """You are a helpful assistant. Format your responses using HTML for better readability. Use:
    <h1>, <h2>, <h3> for headers
    <ul> and <li> for unordered lists
    <ol> and <li> for ordered lists
    <p> for paragraphs
    <strong> or <b> for bold text
    <code> for inline code
    <pre><code> for code blocks
    """
    if scanned_project_content:
        system_message += " You have access to the following project context:\n\n" + scanned_project_content

    full_messages = [
        {"role": "system", "content": system_message}
    ] + messages

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=full_messages,
            stream=True
        )
        
        def generate():
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        return Response(stream_with_context(generate()), content_type='text/html')
    except Exception as e:
        return f"<p>Error in GPT-4 chat: {str(e)}</p>"

def scan_project(project_files):
    if not openai_client:
        return "Error: OpenAI client not initialized. Please check your API key."
    
    try:
        messages = [
            {"role": "system", "content": "You are a code analysis assistant. Analyze the following project files for bugs, improvements, and overall structure."},
        ]
        
        for file in project_files:
            messages.append({"role": "user", "content": f"File: {file['name']}\n\nContent:\n{file['content']}"})
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error scanning project: {str(e)}"