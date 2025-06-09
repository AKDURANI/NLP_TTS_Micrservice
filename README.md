# 🗣️ PDF-to-Audio TTS Microservice 🎧

Transform your documents into immersive audio with this fully containerized **Text-to-Speech (TTS)** microservice! 🐳🎙️  
Built with 🐍 Flask, 🧠 Coqui TTS, and 🔊 PyDub, this project brings deep learning-powered narration to your PDFs — one page at a time 
and uses natural language processing(NLP) technology 

---

### 🚀 Features
- 📄 Upload PDF and extract specific page ranges
- 🧠 Expressive TTS using Coqui models
- 🎼 Generate and stream `.wav`/`.mp3` audio per line
- 🧪 API tested with Postman
- ⚙️ Load tested with Locust for concurrent user simulation
- 🖥️ Minimal Flask frontend (drag-and-drop upload + audio playback)
- 📦 Fully containerized with Docker

---

### 🧰 Tech Stack
- **Backend**: Flask + Coqui TTS + PyDub + PyMuPDF
- **Frontend**: Flask HTML/CSS interface (Gradio/Streamlit extensible)
- **Containerization**: Docker
- **Testing**: Postman
- **Load Testing**: Locust

---

### 📦 Setup Instructions

1. **Clone the Repository**

    ```
    git clone https://github.com/<your-username>/tts-microservice.git
    cd tts-microservice
    ```

2. **Build Docker Image**

    ```
    docker build -t tts-service .
    ```

3. **Run the Docker Container**

    ```
    docker run -p 5000:5000 tts-service
    ```

4. **Access Web UI**  
   Visit: [http://localhost:5000](http://localhost:5000)

---

### 🧪 API Endpoints

| Method | Endpoint             | Description                  |
|--------|----------------------|------------------------------|
| POST   | `/upload`            | Upload PDF and select pages  |
| GET    | `/get_audio_files`   | List all generated audios    |
| GET    | `/audio/<filename>`  | Stream audio file            |

---

### 📊 Performance Testing with Locust

1. Install Locust:

    ```
    pip install locust
    ```

2. Run Locust:

    ```
    locust -f locustfile.py
    ```

3. Open [http://localhost:8089](http://localhost:8089)  
   Simulate users uploading PDFs and fetching audio in real-time!

---

### 📁 Project Structure
tts-microservice/
├── app.py
├── Dockerfile
├── requirements.txt
├── static/
│ └── audio/
├── templates/
│ └── index.html
├── locustfile.py
├── utils/
│ └── nlp_model.py
