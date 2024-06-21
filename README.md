## Jarvis: Your Personal AI Assistant

This repository contains the implementation of Jarvis, a personal AI assistant built using various Python libraries. Jarvis can perform tasks such as responding to greetings, searching Wikipedia, opening web browsers, and interacting using OpenAI's GPT-3.5 model for conversational purposes.

### Features

- Voice interaction using pyttsx3 and SpeechRecognition.
- Wikipedia search integration.
- Web browsing capabilities.
- Conversational abilities powered by OpenAI's GPT-3.5 model.

### Prerequisites

Ensure you have the following installed before running the application:

- Python 3.7 or higher
- Required Python libraries (listed in `requirements.txt`)
- OpenAI API key

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/jarvis-ai-assistant.git
    cd jarvis-ai-assistant
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set your OpenAI API key**:
    - Create a file named `config.py` in the project directory.
    - Add the following line to `config.py`, replacing `your_openai_api_key` with your actual OpenAI API key:
      ```python
      apikey = 'your_openai_api_key'
      ```

### Usage

1. **Run the application**:
    ```sh
    python main.py
    ```

2. **Interact with Jarvis**:
    - Use voice commands to interact with Jarvis.
    - Jarvis can respond to greetings, search Wikipedia, open YouTube or Google, tell the current time, and have conversations using OpenAI's GPT-3.5 model.

### Code Explanation

Here's a brief overview of the code in `main.py`:

1. **Imports and Initializations**:
    - Imports necessary libraries and initializes the text-to-speech engine.
    - Sets up the voice properties for the assistant.

2. **Speak Function**:
    - Converts text to speech using pyttsx3.
    ```python
    def speak(audio):
        engine.say(audio)
        engine.runAndWait()
    ```

3. **Wish Function**:
    - Greets the user based on the current time of day.
    ```python
    def wishme():
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning ")
        elif hour >= 12 and hour < 16:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
        speak("How can I help you today?")
    ```

4. **Chat Function**:
    - Handles the conversation with the user using OpenAI's GPT-3.5 model.
    ```python
    def chat(query):
        global chatStr
        print(chatStr)
        openai.api_key = apikey
        chatStr += f"Saurabh: {query}\n Jarvis: "
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, Saurabh's human assistant. You are witty and full of personality, you can also be sarcastic. Your answers should be limited to 2-3 short sentences"
                },
                {
                    "role": "user",
                    "content": f"{query}"
                }
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        speak(response["choices"][0]['message']['content'])
        return response["choices"][0]['message']['content']
    ```

5. **AI Function**:
    - Generates a response from OpenAI's GPT-3.5 model and saves it to a file.
    ```python
    def ai(prompt):
        openai.api_key = apikey
        text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response["choices"][0]["text"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
            f.write(text)
    ```

6. **Take Command Function**:
    - Listens for voice input from the user and converts it to text.
    ```python
    def takeCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening....")
            r.pause_threshold = 1
            audio = r.listen(source)
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language="en-in")
                print(f"User said: {query}")
                return query
            except Exception as e:
                return "Some Error Occurred. Sorry from Jarvis"
    ```

7. **Main Functionality**:
    - Contains the main loop to continuously listen for and respond to user commands.
    ```python
    if __name__ == "__main__":
        while True:
            query = takeCommand().lower()
            if "hi jarvis" in query:
                speak("Hello Saurabh")
                wishme()
            elif "can you do" in query:
                speak("I can help you with Wikipedia search, I can open Google and YouTube, and also can tell you current time")
            elif "wikipedia" in query:
                query = query.replace("tell me about", "")
                query = query.replace('wikipedia', '')
                speak('Searching on Wikipedia')
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak("According to Wikipedia")
                speak(result)
            elif "open youtube" in query:
                webbrowser.open("youtube.com")
            elif "open google" in query:
                webbrowser.open("google.com")
            elif "current time" in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")
            elif "Using artificial intelligence".lower() in query.lower():
                ai(prompt=query)
            elif "reset chat".lower() in query.lower():
                chatStr = ""
            elif "goodbye" in query:
                speak("Good Bye sir, have a great day ahead!")
                break
            else:
                print("Chatting...")
                chat(query)
    ```

### Requirements

Create a `requirements.txt` file with the following content:

```
datetime
pyttsx3==2.90
SpeechRecognition==3.8.1
wikipedia-api==0.5.4
openai==0.27.0
numpy==1.24.3
```

### Contributing

Contributions are welcome! Please submit a Pull Request with a detailed description of your changes.

### License

This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to customize this README file further as needed. Happy coding!
