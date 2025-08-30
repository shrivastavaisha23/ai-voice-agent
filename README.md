AI Voice Agent – ELARA AI

An interactive AI Voice Agent built with FastAPI, AssemblyAI, MurfAI, and OpenAI, capable of real-time conversation using speech-to-text (STT), text-to-speech (TTS), personas, and special skills.

This project was built as part of the 30 Days of AI Voice Agents Challenge. By @MURFAI

🚀 Features

✅ Speech-to-Text (STT) – Convert spoken input into text using AssemblyAI.
✅ Text-to-Speech (TTS) – Convert AI responses into natural voice using MurfAI.
✅ Conversational AI – Powered by OpenAI LLM for dynamic and intelligent replies.
✅ Persona Mode – Switch between fun personas (e.g., Pirate, Cowboy, Robot).
✅ Special Skills – Agent can fetch weather, news, and web results.
✅ User-Configurable API Keys – Enter your own API keys directly in the UI.
✅ Real-time Web UI – Interactive frontend built with MediaStream API + JavaScript.
✅ Deployment Ready – Hosted on Render for public access.

🛠️ Tech Stack

Backend: FastAPI (Python)

Frontend: HTML, CSS, JavaScript (MediaStream API)

APIs:

AssemblyAI (Speech-to-Text)

MurfAI (Text-to-Speech)

OpenAI (LLM for conversations)

Deployment: Render

📂 Project Structure
voice-agent/
│── main.py          # FastAPI backend  
│── static/
│    ├── index.html  # Frontend UI  
│    ├── script.js   # Handles audio, STT, and TTS  
│    └── style.css   # UI styling  
│── requirements.txt # Python dependencies  
│── README.md        # Documentation  

⚡ Getting Started
1️⃣ Clone the Repository
git clone https://github.com/your-username/voice-agent.git
cd voice-agent

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Backend
uvicorn main:app --reload

4️⃣ Open the Frontend

Simply open static/index.html in your browser.

🔑 Configuration

Before using the agent, you’ll need API keys for:

AssemblyAI API → Get key here

MurfAI API → Get key here

OpenAI API → Get key here

➡️ You can enter these API keys directly in the UI config section.

🌍 Deployment

This project is deployed on Render for public access.


🔮 Future Improvements

Add multilingual support (Hindi, Spanish, etc.)

Build a memory system so the agent remembers past conversations

Improve UI/UX with better styling and animations

Add more special skills (calendar, reminders, finance updates)

🙌 Acknowledgements

This project was built as part of the 30 Days of AI Voice Agents Challenge
.
Special thanks to MurfAI, AssemblyAI, and OpenAI for their APIs.

👩‍💻 Author

Isha Shrivastava
LinkedIn: https://www.linkedin.com/in/isha-shrivastava0604?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app
