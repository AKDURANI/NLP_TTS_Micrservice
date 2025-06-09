from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import grpc
import sys
from collections import deque
import re

# Add the grpc_gen directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'grpc_gen')))
import tts_pb2
import tts_pb2_grpc

app = Flask(__name__)
AUDIO_OUTPUT_DIR = "audio_outputs"
UPLOAD_FOLDER = "uploads"
audio_queue = deque()  # Queue to store audio files
processed_files = set()  # Set to track processed files

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

def natural_sort_key(s):
    # Extract numbers from the filename
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]

class AudioFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.wav'):
            audio_path = event.src_path.replace('\\', '/')
            if audio_path not in processed_files:
                audio_queue.append(audio_path)
                processed_files.add(audio_path)
                print(f"New audio file added to queue: {audio_path}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_audio_files')
def get_audio_files():
    # Get all existing WAV files in the directory
    current_files = [f for f in os.listdir(AUDIO_OUTPUT_DIR) if f.endswith('.wav')]
    
    # Sort files using natural sort
    current_files.sort(key=natural_sort_key)
    
    # Convert to URL paths
    current_files = [f'/audio/{f}' for f in current_files]
    
    # Add any new files from the queue
    while audio_queue:
        file_path = audio_queue.popleft()
        file_name = os.path.basename(file_path)
        if f'/audio/{file_name}' not in current_files:
            current_files.append(f'/audio/{file_name}')
    
    # Sort the final list again to maintain order
    current_files.sort(key=lambda x: natural_sort_key(os.path.basename(x)))
    
    return jsonify({'audio_files': current_files})

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_OUTPUT_DIR, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Save the file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Get page range from form data
    start_page = int(request.form.get('start_page', 1))
    end_page = int(request.form.get('end_page', 1))
    
    try:
        # Call the gRPC service
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = tts_pb2_grpc.TextToSpeechStub(channel)
            grpc_request = tts_pb2.GenerateRequest(
                pdf_path=file_path,
                start_page=start_page,
                end_page=end_page
            )
            response = stub.GenerateAudio(grpc_request)
            
            if response.message == "Success":
                return jsonify({
                    'message': 'File processed successfully',
                    'audio_path': f'/audio/{os.path.basename(response.output_audio_path)}'
                })
            else:
                return jsonify({'error': response.message}), 500
    except Exception as e:
        print(f"Error in upload_file: {str(e)}")
        return jsonify({'error': str(e)}), 500

def start_file_watcher():
    event_handler = AudioFileHandler()
    observer = Observer()
    observer.schedule(event_handler, AUDIO_OUTPUT_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    # Start file watcher in a separate thread
    watcher_thread = threading.Thread(target=start_file_watcher)
    watcher_thread.daemon = True
    watcher_thread.start()
    
    # Start Flask app
    app.run(debug=True, port=5000)