from os import system
import speech_recognition as sr
from gpt4all import GPT4All
import sys
import whisper
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices=AudioUtilities.GetSpeakers()
interface= devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume=cast(interface, POINTER(IAudioEndpointVolume))
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
            output = model.generate(prompt_text, max_tokens=200)
            print('GPT4All: ', output)
            speak(output)
            return output
    except Exception as e:
        print("Prompt error: ", e)
        return "Prompt error"

def search_google(query):
    from googlesearch import search
    search_query = query.split("search for", 1)[1].strip()
    search_results = list(search(query, num=5, stop=5, pause=2))
    print("Search results: ", search_results)
    speak("Search results: ")
    return None

def set_volume(input):
    current=volume.GetMasterVolumeLevel()
    if "volume max" in input.lower():
        volume.SetMasterVolumeLevel(0.0, None)
        print("Volume set: Max")
        speak("Volume set: Max")
    elif "volume minimum" in input.lower():
        volume.SetMasterVolumeLevel(-65.0, None)
        print("Volume set: Minimum")
        speak("Volume set: Minimum")
    elif "volume up" in input.lower() or "volume down" in input.lower():
        if "volume up" in input.lower():
            new_volume = min(current + 6.0, 0.0)
            action = "Increased"
        elif "volume down" in input.lower():
            new_volume = max(current - 6.0, -65.0)
            action = "Decreased"
        volume.SetMasterVolumeLevel(new_volume, None)
        print(f"Volume set: {action}")
        speak(f"Volume set: {action}")
    else:
        print("I don't know what level to set the volume to.")
        speak("I don't know what level to set the volume to.")

def start_listening():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('\nStart speaking. \n')
        while True:
            audio = r.listen(source)
            try:
                user_input = r.recognize_google(audio)
                if "search for" in user_input.lower():
                    search_google(user_input)
                elif "volume" in user_input.lower():
                    set_volume(user_input)
                elif "close the program" in user_input.lower():
                    print("Goodbye")
                    speak("Goodbye")
                    return
                else:
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