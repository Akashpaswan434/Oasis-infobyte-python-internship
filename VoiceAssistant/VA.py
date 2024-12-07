import pyttsx3
import speech_recognition as sr
import pyautogui
import time
import datetime
import wikipedia
import webbrowser
import os
import smtplib

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set the voice to the second available voice

# Dictionary to store email contacts
email_contacts = {
    "friend": "friend@example.com",
    "family": "family@example.com"
}

def speak(output_text):

    engine.say(output_text)
    engine.runAndWait()

def greet_user():

    current_hour = datetime.datetime.now().hour
    if 0 <= current_hour < 12:
        speak("Good Morning!")
    elif 12 <= current_hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    assistant_name = "Hunterdii"
    speak(f"I am {assistant_name}. How may I assist you today?")

def listen_to_user():

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        user_command = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {user_command}")
        return user_command.lower()
    except Exception as error:
        print("Could not understand. Please say that again.")
        return "None"

def send_email(recipient_email, email_content):
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('jestonpatel9879@gmail.com', 'codesownway0707')  # Placeholder credentials
        server.sendmail('jasonhunts0707@gmail.com', recipient_email, email_content)
        server.close()
        speak("Email has been sent!")
    except Exception as error:
        print(error)
        speak("Sorry, I could not send the email.")

if __name__ == "__main__":
    greet_user()
    
    while True:
        command = listen_to_user()

        if 'wikipedia' in command:
            speak('Searching Wikipedia...')
            search_query = command.replace("wikipedia", "")
            results = wikipedia.summary(search_query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in command:
            webbrowser.open("https://youtube.com")

        elif 'open google' in command:
            webbrowser.open("https://google.com")

        elif 'play music' in command:
            music_url = "https://music.youtube.com/playlist?list=PLIL965-SXjbVEiWwe1l6RApWYDnbhc_Oz"
            webbrowser.open(music_url)
            time.sleep(5)
            pyautogui.press('space')

        elif 'the time' in command:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")

        elif 'open code' in command:
            code_file_path = "C:\\Users\\hetpa\\OneDrive\\Desktop\\Python Programs\\server.py"
            os.startfile(code_file_path)

        elif 'search google for' in command:
            search_term = command.replace('search google for', '').strip()
            webbrowser.open(f"https://www.google.com/search?q={search_term}")

        elif 'search youtube for' in command:
            search_term = command.replace('search youtube for', '').strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")

        elif 'send email to' in command:
            try:
                speak("What should I say?")
                email_content = listen_to_user()
                speak("Who should I send it to?")
                recipient_name = listen_to_user()
                recipient_email = email_contacts.get(recipient_name)
                if recipient_email:
                    send_email(recipient_email, email_content)
                else:
                    speak("Recipient not found in contacts.")
            except Exception as error:
                print(error)
                speak("Unable to send the email.")

        elif 'open notepad' in command:
            os.system("notepad.exe")

        elif 'open calculator' in command:
            os.system("calc.exe")

        elif 'open command prompt' in command:
            os.system("cmd.exe")

        elif 'shutdown' in command:
            os.system("shutdown /s /t 1")

        elif 'restart' in command:
            os.system("shutdown /r /t 1")
