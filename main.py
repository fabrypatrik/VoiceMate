from os import system
import speech_recognition as sr
from playsound import playsound
from gpt4all import GPT4All
import sys
import whisper
import warnings
import time
import os

model = GPT4All("C:/Users/Patrik/Desktop/voicemate/gpt4all-falcon-newbpe-q4_0.ggfu", allow_download=False)
r = sr.Recognizer()
tiny_model_path = os.path.expanduser('C:/Users/Patrik/.cache/whisper/tiny.pt')
base_model_path = os.path.expanduser('C:/Users/Patrik/.cache/whisper/base.pt')
tiny_model = whisper.load_model(tiny_model_path)
base_model = whisper.load_model(base_model_path)
mic = sr.Microphone() 

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init() 

def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

def prompt_gpt(prompt_text):
    try:
        if len(prompt_text.strip()) == 0:
            print("Empty prompt. Please speak again.")
            return "Empty prompt. Please speak again."
        else:
            print('You: ' + prompt_text)
            output = model.generate(prompt_text, max_tokens=20)
            print('GPT4All: ', output)
            speak(output)
            return output
    except Exception as e:
        print("Prompt error: ", e)
        return "Prompt error"

def start_listening():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('\nStart speaking. \n')
        while True:
            audio = r.listen(source)
            try:
                user_input = r.recognize_google(audio)
                output = prompt_gpt(user_input)
                # print("GPT4All:", output)
                print('\nContinue speaking. \n')
            except sr.UnknownValueError:
                print('Waiting for you...')
                # print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

if __name__ == '__main__':
    start_listening()