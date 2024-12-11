import pyttsx3
import subprocess
import webbrowser
import speech_recognition as sr
import time
import openai
from datetime import datetime

engine = pyttsx3.init()

recognizer = sr.Recognizer()

openai.api_key = 'sk-fXfzQeaAOFfOo3G7_jLCHV2WjO5Qflygs-7spNOjgYT3BlbkFJbyuc8EQAtWDASWgjfuOJZtDBMwSG7wStnC92LyyfgA' 

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def open_application(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "epic games launcher": r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",  # Adjust path as needed
        "browser": "start chrome",  
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "chess": "https://www.chess.com",
        "facebook": "https//www.facebook.com"
    }

    if app_name in apps:
        app_path = apps[app_name]
        try:
            if app_name in ["youtube", "instagram", "chess", "facebook"]:
                webbrowser.open(app_path)
            else:
                subprocess.Popen(app_path, shell=True)
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"
    else:
        return "Application not recognized."

def listen_to_microphone():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."
        except sr.WaitTimeoutError:
            return "Listening timed out, please try again."

def list_functions():
    functions = (
        "I can do the following:\n"
        "1. Open applications like Notepad, Calculator, Epic Games Launcher, and your browser.\n"
        "2. Open websites like YouTube and Instagram.\n"
        "3. Answer your questions using ChatGPT.\n"
        "4. Listen to your voice commands.\n"
        "5. Speak responses aloud.\n"
        "Just ask me what you need!"
    )
    return functions

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return f"The current time is {current_time}"

def get_creator():
    return "I was created by Sir Nikhil Bajaj and his team, which includes Vardan, Pranav, and Sukhman, who programmed me to assist and make life easier."

def main():
    # Greet the user
    greeting = "Hi Commander, I am listening to your commands."
    print(greeting)
    speak_text(greeting)
    
    while True:

        user_input = listen_to_microphone().lower()

        if user_input:
            if "jarvis" in user_input:
                command = user_input.replace('jarvis', '').strip()

                if command == "goodbye":
                    farewell = "Goodbye, Commander. Shutting down."
                    print(farewell)
                    speak_text(farewell)
                    break

                if command.startswith('open '):
                    app_name = command[5:].strip().lower()
                    response = open_application(app_name)
                elif command == "what can you do":
                    response = list_functions()
                elif command in ["what is the time", "what's the time"]:
                    response = get_current_time()
                elif command in ["who created you", "who made you"]:
                    response = get_creator()
                else:
                    try:
                        response = get_chatgpt_response(command)
                    except Exception as e:
                        response = f"Error: {str(e)}"

                # Print and speak the response
                print(f"Jarvis: {response}")
                speak_text(response)
        
    
        time.sleep(0.4)

if __name__ == "__main__":
    main()
