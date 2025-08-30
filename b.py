import speech_recognition as sr
import requests

ESP_IP = "http://192.168.19.164"  # ESP IP

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Talk now: ")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)  # Convert speech to text
    print("You said:", text)

    # Send text to ESP32
    data = requests.post(ESP_IP + "/voice", json={"msg": text})
    print(data)

except Exception as e:
    print("Error:", e)
