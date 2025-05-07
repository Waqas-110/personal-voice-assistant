import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import PhotoImage
import datetime
import wikipedia
import webbrowser
import os
import time
import random
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import pyautogui
import requests

# GUI start
app = tk.Tk()
app.title("Personal Voice Assistant")
app.geometry("500x600")
app.configure(bg="#D6EAF8")

# Engine initialization
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# --- Common Functions ---

def update_result(text):
    result_label.config(text=text)
    app.update()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    update_result(text)  # Update window as well

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello, Good Morning")
    elif 12 <= hour < 18:
        speak("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")

def takeCommand():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300
    r.pause_threshold = 0.8

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        update_result("Listening...")
        audio = r.listen(source, phrase_time_limit=5)

    try:
        statement = r.recognize_google(audio, language='en-in')
        update_result(f"User said: {statement}")
        speak(f"You said: {statement}")
        return statement
    except sr.UnknownValueError:
        update_result("Could not understand audio")
        speak("Could not understand audio")
        return ""
    except sr.RequestError as e:
        update_result(f"Could not request results; {e}")
        speak("Could not understand audio")
        return ""

def game_play():
    speak("Let's play Rock Paper Scissors! Best of five rounds.")
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    comp_score = 0

    for i in range(5):
        speak(f"Round {i+1}. Please say rock, paper, or scissors.")
        user_choice = takeCommand().lower()
        comp_choice = random.choice(choices)

        if user_choice not in choices:
            speak("Invalid choice, round forfeited.")
        else:
            speak(f"You chose {user_choice}, computer chose {comp_choice}.")
            if user_choice == comp_choice:
                speak("It's a tie.")
            elif (user_choice == "rock" and comp_choice == "scissors") or \
                 (user_choice == "paper" and comp_choice == "rock") or \
                 (user_choice == "scissors" and comp_choice == "paper"):
                speak("You win this round.")
                user_score += 1
            else:
                speak("Computer wins this round.")
                comp_score += 1

    speak(f"Final score: You {user_score}, Computer {comp_score}.")
    if user_score > comp_score:
        speak("Congratulations, you won the game!")
    elif comp_score > user_score:
        speak("Computer won the game. Better luck next time.")
    else:
        speak("The game is a tie.")

def search_youtube(query):
    webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={query}")
    speak(f"Searching YouTube for {query}")
    time.sleep(5)

def search_google(query):
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}")
    time.sleep(5)

def close_current_window():
    speak("Closing the current window")
    pyautogui.hotkey('alt', 'f4')

# --- Main Mic Click Function ---

def on_mic_click():
    statement = takeCommand().lower()

    if any(word in statement for word in ["bye", "good", "stop", "tata"]):
        speak('Your personal assistant is shutting down. Goodbye!')
        app.quit()

    elif 'game' in statement or 'rock paper scissors' in statement:
        game_play()

    elif 'wikipedia' in statement:
        speak('Searching Wikipedia...')
        statement = statement.replace("wikipedia", "")
        results = wikipedia.summary(statement, sentences=3)
        speak("According to Wikipedia")
        speak(results)

    elif 'open youtube' in statement:
        webbrowser.open_new_tab("https://www.youtube.com")
        speak("YouTube is open now")
        time.sleep(5)

    elif 'open google' in statement:
        webbrowser.open_new_tab("https://www.google.com")
        speak("Google Chrome is open now")
        time.sleep(5)

    elif 'open gmail' in statement:
        webbrowser.open_new_tab("gmail.com")
        speak("Google Mail is open now")
        time.sleep(5)

    elif 'time' in statement:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'who are you' in statement or 'what can you do' in statement:
        speak("I am a personal assistant created by Waqas Anwar. I can help you with searching, calculations, playing games, and more.")

    elif "who made you" in statement or "who created you" in statement:
        speak("I was built by Waqas Anwar.")

    elif 'search on youtube' in statement:
        query = statement.replace("search on youtube", "").strip()
        search_youtube(query)

    elif 'search on google' in statement:
        query = statement.replace("search on google", "").strip()
        search_google(query)

    elif "camera" in statement or "take a photo" in statement:
        ec.capture(0, "robo camera", "img.jpg")
        speak("Photo taken!")

    elif 'search' in statement:
        query = statement.replace("search", "").strip()
        webbrowser.open_new_tab(query)
        time.sleep(5)

    elif 'ask' in statement:
        speak('I can answer computational and geographical questions. What question do you want to ask now?')
        question = takeCommand()
        app_id = "R2K75H-7ELALHR35X"
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        speak(answer)

    elif "log off" in statement or "sign out" in statement:
        speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
        subprocess.call(["shutdown", "/l"])

    elif "close" in statement or "back" in statement:
        close_current_window()

    elif "farther" in statement:
        speak("Waqas Anwar")

    else:
        speak("I did not understand. Please try again.")

# --- GUI Layout ---

title_label = tk.Label(app, text="My Voice Assistant", font=("Arial", 20, "bold"), bg="#D6EAF8", fg="darkblue")
title_label.pack(pady=20)

mic_image = PhotoImage(file="mic.png")
mic_button = tk.Button(app, image=mic_image, command=on_mic_click, bd=0, bg="#D6EAF8", activebackground="#D6EAF8")
mic_button.pack(pady=20)

result_label = tk.Label(app, text="Mic par click karo aur bolna shuru karo...", font=("Arial", 14), bg="#D6EAF8", wraplength=400, justify="center")
result_label.pack(pady=20)

# Start assistant
speak("Loading your personal assistant")
wishMe()

app.mainloop()
