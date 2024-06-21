import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
#from langchain import PromptTemplate, HuggingFaceHub,LLMChain
import os
import openai
from config import apikey
import random
import numpy as np

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.getProperty('voices')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning ")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("How can I help you today?")

chatStr = ""

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
        #prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )
    # todo: Wrap this inside of a  try catch block
    speak(response["choices"][0]['message']['content'])
    return response["choices"][0]['message']['content']

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
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)



# it takes microphone input from user and return string output
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold =  1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio,language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "hi jarvis" in query:
            speak("Hello Saurabh")
            wishme()

        elif "can you do" in query:
            speak("I can help ypu with wikipedia search, I can open Google and youtube and also can tell you current time")

        elif "wikipedia" in query:
            query= query.replace("tell me about", "")
            query = query.replace('wikipedia','')
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




