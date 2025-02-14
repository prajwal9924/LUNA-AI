import speech_recognition as sr
import pyttsx3
import openai
from datetime import datetime
import pyjokes
import random
import pywhatkit as kit
import wikipedia

# Initialize text-to-speech engine
engine = pyttsx3.init()


# Set the assistant's voice to female
def set_female_voice():
    voices = engine.getProperty('voices')  # Get available voices
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():  # Look for a female voice
            engine.setProperty('voice', voice.id)
            print(f"Voice set to: {voice.name}")
            break
    else:
        print("Female voice not found. Using default voice.")


# Apply the female voice
set_female_voice()

# Set your OpenAI API key (replace with your actual API key)
openai.api_key = 'your-openai-api-key'


# Function for text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to recognize speech
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Request error: {e}")
            return ""


# Function to wait for the wake word "Luna"
def wait_for_luna():
    while True:
        print("Waiting for 'Luna'...")
        command = listen()
        if "luna" in command:
            speak("Yes, I'm here. How can I help you?")
            return  # Return control to main command processing


# Function to process commands
def process_command(command):
    if "hello" in command:
        response = "Hello! How can I assist you today?"
        speak(response)
    elif "what is your name" in command:
        response = "I am your voice assistant, Luna."
        speak(response)
    elif "thanks" in command:
        response = "Goodbye! Have a great day!"
        speak(response)
        return False
    elif "date" in command or "time" in command:
        tell_date_time(command)
    elif "joke" in command:
        tell_joke()
    elif "story" in command:
        tell_story()
    elif "explain" in command or "what is" in command or "tell me about" in command:
        explain_topic(command)
    elif "play" in command and "on youtube" in command:
        play_youtube_video(command)
    elif "audio explanation" in command:
        provide_audio_explanation(command)
    else:
        response = "I'm not sure how to help with that."
        speak(response)
    return True


# Function to provide an audio explanation
def provide_audio_explanation(command):
    try:
        topic = command.replace("audio explanation", "").strip()
        if not topic:
            speak("Please tell me the topic you want me to explain.")
            topic = listen()  # Wait for the user to say the topic

        if topic:
            speak(f"Let me explain {topic}.")
            explanation = ask_gpt(f"Explain {topic} in simple terms.")
            print(f"Explanation: {explanation}")
            speak(explanation)  # Speak the explanation
        else:
            speak("I didn't hear any topic. Please try again.")
    except Exception as e:
        print(f"Error providing audio explanation: {e}")
        speak("Sorry, I couldn't provide an explanation.")


# Function to use GPT for generating responses
def ask_gpt(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Sorry, I couldn't process your request."


# Function to tell the current date and time
def tell_date_time(command):
    now = datetime.now()
    if "time" in command:
        current_time = now.strftime("%I:%M %p")  # Format: 12-hour clock
        response = f"The current time is {current_time}."
        print(response)
        speak(response)
    if "date" in command:
        current_date = now.strftime("%A, %B %d, %Y")  # Format: Day, Month Date, Year
        response = f"Today's date is {current_date}."
        print(response)
        speak(response)


# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()  # Get a random joke
    print(f"Joke: {joke}")
    speak(joke)


# Function to tell a story
def tell_story():
    stories = [
        "Once upon a time, in a forest far away, there was a clever fox who outwitted a hungry lion. The fox pretended to lead the lion to a feast, but instead, he tricked him into falling into a trap. The fox learned that intelligence often triumphs over brute force.",
        "Long ago, in a village nestled in the mountains, there was a kind old man who would fix broken toys for children. One day, he fixed a doll that turned out to be magical, granting him a wish. The man wished for happiness for his village, and from then on, the village prospered with joy and laughter.",
        "In a bustling city, a little robot named Sparky dreamed of becoming an artist. Though people doubted him, Sparky worked tirelessly and painted a mural that amazed everyone. Sparky proved that with passion and perseverance, anything is possible.",
    ]
    story = random.choice(stories)  # Select a random story
    print(f"Story: {story}")
    speak(story)


# Function to explain a topic with TTS
def explain_topic(command):
    try:
        if "detailed" in command:
            topic = command.replace("explain in detail", "").strip()
            response = kit.info(topic, lines=10)  # Fetch detailed explanation (10 lines)
        else:
            topic = command.replace("explain", "").strip()
            topic = topic.replace("what is", "").strip()
            topic = topic.replace("tell me about", "").strip()
            response = wikipedia.summary(topic,3)  # Fetch brief explanation (3 lines)

        print(f"Explanation: {response}")
        speak("Here's what I found:")
        speak(response)  # Use TTS to read the explanation
    except Exception as e:
        print(f"Error fetching information: {e}")
        response = "Sorry, I couldn't fetch the information you requested."
        speak(response)


# Function to play a YouTube video
def play_youtube_video(command):
    try:
        topic = command.replace("play", "").replace("on youtube", "").strip()
        speak(f"Playing {topic} on YouTube.")
        kit.playonyt(topic)  # Search and play the video on YouTube
    except Exception as e:
        print(f"Error playing YouTube video: {e}")
        speak("Sorry, I couldn't play the video.")


# Main loop
if _name_ == "_main_":
    speak("Hi! Say 'Luna' to activate me.")
    while True:
        wait_for_luna()
        while True:
            user_command = listen()
            if user_command:
                if not process_command(user_command):
                    break