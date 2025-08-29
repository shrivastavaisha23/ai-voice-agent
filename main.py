# main.py

import os
import json
import logging
import uuid
from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import google.generativeai as genai
from dotenv import load_dotenv
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

# Load environment variables from .env file
load_dotenv()

# Set up logging for better debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask and Flask-Sock
app = Flask(__name__)
sock = Sock(app)

# API Keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLY_API_KEY = os.getenv("ASSEMBLY_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# In-memory chat history (Day 10)
# A more robust solution for a real application would use a database.
chat_histories = {}

# --- API Endpoints and WebSocket Handlers ---

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/api/config', methods=['POST'])
def update_config():
    """
    Endpoint to receive API keys from the client and set them as environment variables.
    """
    data = request.json
    api_keys = {
        'gemini': data.get('gemini_api_key'),
        'murf': data.get('murf_api_key'),
        'assembly': data.get('assembly_api_key'),
        'news': data.get('news_api_key'),
        'openweather': data.get('openweather_api_key')
    }
    
    for key, value in api_keys.items():
        if value:
            os.environ[f"{key.upper()}_API_KEY"] = value
    
    # Re-configure Gemini with the new key if provided
    if api_keys['gemini']:
        genai.configure(api_key=api_keys['gemini'])
    
    return jsonify({"status": "success", "message": "API keys updated."}), 200


@sock.route('/ws')
def voice_agent_websocket(ws):
    """
    Handles the core voice agent logic via a WebSocket connection.
    This endpoint orchestrates LLM and TTS streaming.
    (Days 15-23)
    """
    logging.info("WebSocket connection established.")
    
    # Check for API keys at the start of the connection
    api_keys_present = {
        "gemini": bool(os.getenv("GEMINI_API_KEY")),
        "murf": bool(os.getenv("MURF_API_KEY")),
        "assembly": bool(os.getenv("ASSEMBLY_API_KEY")),
        "news": bool(os.getenv("NEWS_API_KEY")),
        "openweather": bool(os.getenv("OPENWEATHER_API_KEY"))
    }
    
    for key, present in api_keys_present.items():
        if not present:
            logging.warning(f"Warning: {key.upper()} API key not set on server.")
    
    if not api_keys_present['gemini']:
        ws.send(json.dumps({"type": "error", "message": "Server error: Gemini API key not set. Please enter it in the UI."}))
        return

    # Initialize Gemini client
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    
    # Define the persona and initial instructions for the agent (Day 24, 25)
    system_instruction = f"""
    You are Elara, an AI voice agent with a friendly and helpful persona. Your main goal is to assist the user with their queries.
    
    You have a special skill:
    1. You can search the web using the 'google_search' tool. Use this tool whenever a user asks for up-to-date information, news, or facts that require real-time data from the internet.

    You should be concise and conversational. Keep your responses under 150 characters to ensure a smooth voice experience.
    """
    
    # Get session ID and manage chat history
    session_id = request.args.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
    
    if session_id not in chat_histories:
        chat_histories[session_id] = []
    
    # The main WebSocket loop
    try:
        while True:
            message = ws.receive()
            if not message:
                continue

            try:
                data = json.loads(message)
                message_type = data.get('type')
                
                if message_type == 'transcript':
                    user_transcript = data.get('text')
                    if not user_transcript:
                        continue
                    
                    logging.info(f"Received transcript: {user_transcript}")

                    # Append user message to chat history
                    chat_histories[session_id].append({"role": "user", "parts": [{"text": user_transcript}]})

                    # Prepare LLM payload with chat history
                    llm_payload = {
                        "contents": [
                            {"role": "user", "parts": [{"text": system_instruction}]},
                            *chat_histories[session_id]
                        ],
                        "tools": [{"google_search": {}}]
                    }
                    
                    # Stream LLM response (Day 19)
                    full_llm_response = ""
                    for chunk in model.generate_content(llm_payload["contents"], tools=llm_payload["tools"], stream=True):
                        try:
                            text_chunk = chunk.candidates[0].content.parts[0].text
                            full_llm_response += text_chunk
                            # Send partial response to client for display
                            ws.send(json.dumps({"type": "llm_chunk", "text": text_chunk}))
                        except (AttributeError, IndexError):
                            # Handle cases where the chunk does not contain text
                            continue

                    if full_llm_response:
                        # Append LLM response to chat history
                        chat_histories[session_id].append({"role": "model", "parts": [{"text": full_llm_response}]})

                        # Stream TTS audio (Day 20, 22)
                        logging.info("Starting TTS streaming...")
                        tts_payload = {
                            "contents": [{"parts": [{"text": full_llm_response}]}],
                            "generationConfig": {
                                "responseModalities": ["AUDIO"],
                                "speechConfig": {
                                    "voiceConfig": {
                                        "prebuiltVoiceConfig": {"voiceName": "Fenrir"}
                                    }
                                }
                            },
                            "model": "gemini-2.5-flash-preview-tts"
                        }
                        
                        try:
                            # Use a non-streaming call for the TTS model
                            response = genai.generate_content(
                                tts_payload["contents"],
                                generation_config=tts_payload["generationConfig"],
                                model=tts_payload["model"],
                            )
                            audio_data_base64 = response.candidates[0].content.parts[0].inline_data.data
                            ws.send(audio_data_base64, binary=True)
                            
                            logging.info("TTS stream complete.")

                        except Exception as e:
                            logging.error(f"TTS API request failed: {e}")
                            ws.send(json.dumps({"type": "error", "message": "I'm having trouble generating a voice response."}))
                    
                elif message_type == 'clear_history':
                    chat_histories[session_id] = []
                    logging.info("Chat history cleared.")

            except json.JSONDecodeError:
                logging.error("Failed to decode JSON message.")
                ws.send(json.dumps({"type": "error", "message": "Invalid message format."}))
                
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        ws.send(json.dumps({"type": "error", "message": "An unexpected server error occurred."}))
    finally:
        logging.info("WebSocket connection closed.")

if __name__ == '__main__':
    # Configure the server to handle both HTTP and WebSocket requests
    http_server = WSGIServer(('', 5003), app, handler_class=WebSocketHandler)
    http_server.serve_forever()