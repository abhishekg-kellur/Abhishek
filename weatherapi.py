from tkinter import *
import speech_recognition as sr
import pyttsx3
from PIL import ImageTk, Image
import requests
#from pygame import *
import json

window = Tk()
window.title('Weather App')
window.geometry("800x800")
window.resizable(0,0)
heading=Label(window,text="Weather Forecasting App",font="arial 20 bold",bg="black",fg="lightblue").pack(pady="10")
image=Image.open("img.png")
img=image.resize((200,150))
photo=PhotoImage(img)
image_label=Label(window,image=photo).pack(pady="10")
climate_1 = Label(window, text="", font="arial 16 bold")
climate_1.place(x=500, y=500)

description_1 = Label(window, text="", font="arial 16 bold")
description_1.place(x=500, y=530)

temperature_1 = Label(window, text="", font="arial 16 bold")
temperature_1.place(x=500, y=560)

pressure_1 = Label(window, text="", font="arial 16 bold")
pressure_1.place(x=500, y=590)
city_input=StringVar()
input1=Entry(window,font="arial 20 italic",bg="white",fg="lightblue").pack(pady="30")
def display_weather():
    api_key = "e0d91f9cbf1e3b4a51dc8dd7f31e57a1"
    city_name=city_input.get()
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&appid='+api_key
    response = requests.get(weather_url)
    weather_info = response.json()
    kelvin=273.15
    climate_1.config(text=weather_info["weather"][0]["main"])
    description_1.config(text=weather_info["weather"][0]["description"])
    temperature_1.config(text=str(int(weather_info["main"]["temp"]-kelvin)))
    pressure_1.config(text=weather_info["main"]["pressure"])

def run_voice():
    #mixer.init()
    #mixer.music.load('chime1.mp3')
    #mixer.music.play()

    r = sr.Recognizer()
    r.pause_threshold = 0.7
    r.energy_threshold = 400

    with sr.Microphone() as source:

        try:

            audio = r.listen(source, timeout=5)
            message = str(r.recognize_google(audio))
            #mixer.music.load('chime2.mp3')
            #mixer.music.play()
            input1.focus()
            input1.delete(0, END)
            input1.insert(0, message)

        except sr.UnknownValueError:
            print("Could not recognize")
            
        else:
            pass
    
#voice input button
icon=Image.open("mic.png").resize((30,30))
micicon=ImageTk.PhotoImage(icon)
mic_button=Button(window,image=micicon,command=run_voice,overrelief='groove',relief='sunken').place(x=552,y=258)


climate=Label(window,text="Weather Climate",font="arial 16 bold").place(x=150,y=500)
description=Label(window,text="Weather Description",font="arial 16 bold").place(x=150,y=530)
temperature=Label(window,text="Temperature",font="arial 16 bold").place(x=150,y=560)
pressure=Label(window,text="Pressure",font="arial 16 bold").place(x=150,y=590)
button=Button(window,text="Check Weather",command=display_weather,bg="lightblue",fg="black",font="arial 20 bold").place(x=280,y=350)

window.mainloop()