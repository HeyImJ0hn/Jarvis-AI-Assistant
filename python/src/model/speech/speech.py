import speech_recognition as sr
import os
from playsound import playsound
import edge_tts

class SpeechRecog:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.should_process = False

    def speak_text(self, text):
        temp = 'temp.mp3'
        communicate = edge_tts.Communicate(text, "en-GB-RyanNeural")
        communicate.save_sync(temp)
        playsound(temp)
        os.remove(temp)

    def run(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(self.microphone, duration=0.2)
            print("Listening...")
            self.audio = self.recognizer.listen(source)
            if self.should_process:
                pass # TODO: Process the audio
        try:
            print("Recognizing...")
            return self.recognizer.recognize_google(self.audio)
            #self.speak_text(text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {e}")