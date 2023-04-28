import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from PIL import ImageTk, Image, ImageOps
import requests
from io import BytesIO
import speech_recognition as sr
import pyttsx3

YOUR_API_KEY = "e0d91f9cbf1e3b4a51dc8dd7f31e57a1"

root = ttk.Window(themename="solar")
root.title('Weather App')
root.geometry("1920x1080")
root.resizable(0, 0)
#voice output
r = sr.Recognizer()
#voice output necessary requirement
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # adjust the speed, default is 200
engine.setProperty('volume', 0.7)  # adjust the volume, default is 1.0
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #0-male voice, 1-female voice

#engine.say("Hello",self.des,self.wind,self.temp,self.pressure,self.kel,self.water)

#voice input
def input_voice(event):
    r.pause_threshold = 0.9
    r.energy_threshold = 600

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.3)
        audio = r.listen(source, timeout=5)
        try:
            message = r.recognize_google(audio)
            print(message)
            input_field.delete(0, END)
            input_field.insert(0, message)
            get_weather_data()
        except sr.UnknownValueError:
            print("Could not recognize")
            input_field.delete(0, END)
            input_field.insert(0, "Not found")
        else:
            pass

default_icon_data = requests.get('https://openweathermap.org/img/wn/10d@4x.png').content
default_icon_image = Image.open(BytesIO(default_icon_data)).convert('RGBA')
default_icon_photo = ImageTk.PhotoImage(default_icon_image.resize((500, 500)))
# Load the image data and create a PIL Image object
wind_icon_data = requests.get(
    'https://www.iconarchive.com/download/i133595/bootstrap/bootstrap/Bootstrap-wind.512.png').content
wind_icon_image = Image.open(BytesIO(wind_icon_data)).convert('RGBA')
wind_icon_photo = ImageTk.PhotoImage(wind_icon_image.resize((200, 200)))

# style
style = ttk.Style()
style.configure('TEntry', borderwidth=0)
# Create a label and input field using ttk widgets
label1 = ttk.Label(root, text="Right now in ", font="helvatica 16 bold ")
input_field = ttk.Entry(root, width=15, bootstyle="light", font="helvatica 16 bold ", style='TEntry')
input_field.bind("<Button-1>", input_voice)
label2 = ttk.Label(root, text=" , it's  ", font="helvatica 16 bold ")
image_label = ttk.Label(root, image=default_icon_photo)
wind_label = ttk.Label(root, text='\uf89b', font='helvatica 30')
wind_label_data = ttk.Label(root, text='-- m/s', font='helvatica 30')
temp_label = ttk.Label(root, text='\uf2c8', font='helvatica 30')
pre_label = ttk.Label(root, text='\uf140', font='helvatica 30')
pre_label_data = ttk.Label(root, text="-- pa  ", font='helvatica 30')
water_label = ttk.Label(root, text='\uf043', font='helvatica 30')
water_label_data = ttk.Label(root, text='-- %', font='helvatica 30')
temp_label_data = ttk.Label(root, text='--', font='helvatica 120 bold')
temp_label_unit = ttk.Label(root, text='°C', font='helvatica 20')
temp_label_data_kel = ttk.Label(root, text='-- K', font='helvatica 30')

# Pack the label and input field widgets

label1.grid(row=0, column=1, padx=(20, 0), pady=130, sticky="N")
input_field.grid(row=0, column=2, padx=5, pady=130, sticky="N", )
input_field.focus()
label2.grid(row=0, column=5, padx=(0, 20), pady=130, sticky="N")

image_label.grid(row=2, column=0, rowspan=5, sticky="nsew")
temp_label_data.grid(row=2, column=1, rowspan=5, sticky="nsew")
temp_label_unit.grid(row=2, column=2, rowspan=5)
wind_label.grid(row=2, column=4)
wind_label_data.grid(row=2, column=5)
temp_label.grid(row=3, column=4)
temp_label_data_kel.grid(row=3, column=5)
pre_label.grid(row=4, column=4)
pre_label_data.grid(row=4, column=5)
water_label.grid(row=5, column=4)
water_label_data.grid(row=5, column=5)

# Create labels for the second column


# Let the input field control its own size
input_field.pack_propagate(False)

# Bind the <Key> event to a function that updates the width of the input field
def update_width(event):
    input_field.config(width=max(len(input_field.get()) + 2, 3))

def get_weather_data():
    # Get the location entered in the input field
    location = input_field.get()

    # Make a GET request to the OpenWeather API
    response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={YOUR_API_KEY}")
    print(f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={YOUR_API_KEY}")
    # Parse the response JSON and retrieve the temperature
    weather_data = response.json()
    des = weather_data["weather"][0]["description"]
    wind = weather_data["wind"]["speed"]
    temp = round((int(weather_data['main']['temp']) - 273.15))
    kel = weather_data['main']['temp']
    icon_code = weather_data["weather"][0]["icon"]
    pressure = weather_data['main']['pressure']
    water = weather_data['main']['humidity']

    # Convert the temperature from Kelvin to Celsius and update the label
    label2.config(text=f", it's {des}", font="helvatica 16 bold ")
    wind_label_data.config(text=f"{wind} m/s")
    temp_label_data.config(text=f'{temp}')
    pre_label_data.config(text=f'{pressure} hPa')
    temp_label_data_kel.config(text=f'{kel} K')
    water_label_data.config(text=f'{water} %')
    icon_data = requests.get(f'https://openweathermap.org/img/wn/{icon_code}@4x.png').content
    icon_image = Image.open(BytesIO(icon_data)).convert('RGBA')
    #outputting voice of weather
    engine.say(f"The weather in {location} is {des} with {temp} degree celsius")
    engine.say(f"Wind speed of {wind} miles/second humidity {water} degree")
    engine.runAndWait()
    icon_photo = ImageTk.PhotoImage(icon_image.resize((500, 500), resample=Image.BICUBIC), )
    image_label.config(image=icon_photo).update

input_field.bind("<Key>", update_width)
input_field.bind("<Return>", lambda event: get_weather_data())
root.mainloop()