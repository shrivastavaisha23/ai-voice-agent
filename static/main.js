document.addEventListener('DOMContentLoaded', (event) => {
    // DOM Elements
    const apiKeyInput = document.getElementById('apiKey');
    const micContainer = document.getElementById('mic-container');
    const micIcon = document.getElementById('mic-icon');
    const pulseCircle = document.getElementById('pulse-circle');
    const statusMessage = document.getElementById('status-message');
    const chatHistory = document.getElementById('chat-history');
    const messageBox = document.getElementById('message-box');
    const messageText = document.getElementById('message-text');

    // State variables
    let isListening = false;
    let ws;
    let audioContext;
    let audioQueue = [];
    let isSpeaking = false;
    let sessionId;
    
    // Web Speech API for transcription
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.continuous = true;

    // Load API key from local storage on startup (Day 27)
    window.onload = () => {
        const storedKey = localStorage.getItem('geminiApiKey');
        if (storedKey) {
            apiKeyInput.value = storedKey;
        }
        sessionId = localStorage.getItem('voiceAgentSessionId') || generateSessionId();
        localStorage.setItem('voiceAgentSessionId', sessionId);
        setStatus('Click the microphone to start talking.');
    };

    // --- UI & State Management ---

    function generateSessionId() {
        return 'session_' + Date.now();
    }

    function showMessage(message, isError = true) {
        messageText.textContent = message;
        messageBox.style.opacity = '1';
        messageBox.style.pointerEvents = 'auto';
        messageBox.style.backgroundColor = isError ? 'rgba(220, 38, 38, 0.8)' : 'rgba(34, 197, 94, 0.8)';
        setTimeout(() => {
            hideMessage();
        }, 5000);
    }

    function hideMessage() {
        messageBox.style.opacity = '0';
        messageBox.style.pointerEvents = 'none';
    }

    function toggleConfig() {
        const configContent = document.getElementById('config-content');
        const toggleIcon = document.getElementById('config-toggle-icon');
        configContent.classList.toggle('hidden');
        toggleIcon.classList.toggle('fa-chevron-down');
        toggleIcon.classList.toggle('fa-chevron-up');
    }

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'ai-message';
        messageDiv.textContent = text;
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function clearChatHistory() {
        chatHistory.innerHTML = '';
        localStorage.removeItem('voiceAgentSessionId');
        sessionId = generateSessionId();
        localStorage.setItem('voiceAgentSessionId', sessionId);
        showMessage('Chat history cleared!', false);
    }

    function setStatus(text, listening = false, speaking = false) {
        statusMessage.textContent = text;
        isListening = listening;
        isSpeaking = speaking;

        if (isListening) {
            micIcon.classList.remove('fa-microphone');
            micIcon.classList.add('fa-spin', 'fa-microphone-lines');
            pulseCircle.classList.remove('hidden');
        } else if (isSpeaking) {
            micIcon.classList.remove('fa-microphone-lines');
            micIcon.classList.add('fa-microphone');
            micIcon.classList.add('fa-beat');
            pulseCircle.classList.remove('hidden');
        } else {
            micIcon.classList.remove('fa-spin', 'fa-microphone-lines', 'fa-beat');
            micIcon.classList.add('fa-microphone');
            pulseCircle.classList.add('hidden');
        }
    }
    
    // --- WebSocket and Audio Logic ---
    async function startListening() {
        // Stop any previous recognition
        if (isListening) {
            recognition.stop();
        }
        
        const apiKey = apiKeyInput.value;
        if (!apiKey) {
            showMessage('Please enter your Gemini API Key.', true);
            return;
        }
        localStorage.setItem('geminiApiKey', apiKey);

        // Update API key on the server (Day 27)
        try {
            const response = await fetch('/api/config', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ api_key: apiKey })
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.message);
            }
        } catch (error) {
            showMessage('Error updating server config: ' + error.message);
            setStatus('Click the microphone to start talking.');
            return;
        }
        
        setStatus('Connecting...', true);

        // Setup WebSocket connection (Day 15)
        ws = new WebSocket(`ws://localhost:5000/ws?session_id=${sessionId}`);
        
        ws.onopen = async () => {
            console.log('WebSocket connected.');
            setStatus('Listening...');
            recognition.start();
        };

        // Handle transcription from Web Speech API
        recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript;
            console.log('User said:', transcript);
            
            // Send transcript to server when the user stops talking
            if (event.results[event.results.length - 1].isFinal) {
                recognition.stop();
                setStatus('Processing...');
                ws.send(JSON.stringify({ type: 'transcript', text: transcript }));
            }
        };

        // Handle messages from the server
        ws.onmessage = (event) => {
            const message = event.data;
            if (typeof message === 'string') {
                try {
                    const data = JSON.parse(message);
                    if (data.type === 'llm_chunk') {
                        // Display LLM response as it arrives
                        appendMessage(data.text, 'ai');
                    } else if (data.type === 'error') {
                        showMessage(data.message);
                        ws.close();
                    }
                } catch (e) {
                    console.error('Failed to parse JSON:', e);
                }
            } else if (message instanceof Blob) {
                // Play the audio data received from the server (Day 22)
                const audioUrl = URL.createObjectURL(message);
                const audio = new Audio(audioUrl);
                audio.play();
                audio.onended = () => {
                    // Start listening again after the response is played
                    setStatus('Click the microphone to start talking.');
                };
            }
        };

        recognition.onend = () => {
            if (isListening) {
                setStatus('Click the microphone to start talking.');
            }
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            if (event.error !== 'no-speech' && event.error !== 'aborted') {
                showMessage('Speech recognition error: ' + event.error);
            }
            setStatus('Click the microphone to start talking.');
            if (ws) ws.close();
        };

        ws.onclose = () => {
            console.log('WebSocket closed.');
            setStatus('Click the microphone to start talking.');
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            showMessage('WebSocket connection error.', true);
        };
    }

    // --- Event Listeners ---
    micContainer.addEventListener('click', () => {
        if (isListening) {
            recognition.stop();
            if (ws) ws.close();
        } else {
            startListening();
        }
    });
});
