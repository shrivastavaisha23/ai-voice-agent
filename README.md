**AI Voice Agent – ELARA AI**

An interactive AI Voice Agent built with FastAPI, AssemblyAI, MurfAI, and OpenAI, capable of real-time conversation using speech-to-text (STT), text-to-speech (TTS), personas, and special skills.


![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![WebSockets](https://img.shields.io/badge/WebSockets-Supported-orange)
![AssemblyAI](https://img.shields.io/badge/AssemblyAI-STT-red)
![Gemini](https://img.shields.io/badge/Gemini-LLM-purple)
![Murf](https://img.shields.io/badge/Murf-TTS-yellow)


**This project was built as part of the 30 Days of AI Voice Agents Challenge. By @MURFAI**


## 📌 Project Overview
The **AI Voice Agent ELARAAI** enables real-time **speech-to-speech interaction**.  
It records audio, transcribes it with **AssemblyAI**, processes with **Gemini LLM**,  
and speaks back with **Murf TTS**.  

---


## 🚀 Features
- 🎤 **Voice Input** → Records audio in real-time.  
- 📝 **Speech-to-Text (STT)** → AssemblyAI for transcription.  
- 🧠 **AI Reasoning** → Gemini LLM handles queries.  
- 🔊 **Text-to-Speech (TTS)** → Murf converts responses.  
- 🌐 **Web Search Integration** → Optional external info.  
- 💾 **Chat History Storage** → Keeps logs.  
- ⚡ **FastAPI + WebSockets** → Real-time interaction.
 

**🛠️ Tech Stack**

Backend: FastAPI (Python)

Frontend: HTML, CSS, JavaScript (MediaStream API)

APIs:

AssemblyAI (Speech-to-Text)

MurfAI (Text-to-Speech)

OpenAI (LLM for conversations)

Deployment: Render

**Project Structure**
  voice-agent/
│── main.py          # FastAPI backend  
│── static/
│    ├── index.html  # Frontend UI  
│    ├── script.js   # Handles audio, STT, and TTS  
│    └── style.css   # UI styling  
│── requirements.txt # Python dependencies  
│── README.md        # Documentation  


**⚡ Getting Started**

1️⃣ Clone the Repository
git clone https://github.com/your-username/voice-agent.git
cd voice-agent

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Backend
uvicorn main:app --reload

4️⃣ Open the Frontend

Simply open static/index.html in your browser.

**🔑 Configuration**

Before using the agent, you’ll need API keys for:

AssemblyAI API → Get key here

MurfAI API → Get key here

OpenAI API → Get key here

➡️ You can enter these API keys directly in the UI config section.

**🌍 Deployment**

This project is deployed on Render for public access.


**🔮 Future Improvements**

Add multilingual support (Hindi, Spanish, etc.)

Build a memory system so the agent remembers past conversations

Improve UI/UX with better styling and animations

Add more special skills (calendar, reminders, finance updates)

**🙌 Acknowledgements**

This project was built as part of the 30 Days of AI Voice Agents Challenge By MURFAI
.
Special thanks to MurfAI, AssemblyAI, and OpenAI for their APIs.

**👩‍💻 Author**

**Isha Shrivastava**
LinkedIn: https://www.linkedin.com/in/isha-shrivastava0604?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app
