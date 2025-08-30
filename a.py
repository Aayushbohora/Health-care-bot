import requests
import speech_recognition as sr 

a = sr.Recognizer()
b = int(input("Enter the number of requests: "))

with sr.Microphone() as source:
    print("Please speak now:")
    audio = a.listen(source)

for i in range(1, b + 1):
    try:
        response = requests.get(audio)
        if response.status_code == 200:
            print(f"Request {i}: Success")
            time.sleep(1)  # Sleep for 1 second between requests
        else:
            print(f"Request {i}: Failed with status {response.status_code}")
    except Exception as e:
        print(f"Request {i}: Error -> {e}")
