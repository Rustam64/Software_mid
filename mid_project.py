# import necessary modules
from tkinter import *
import urllib.parse
import requests
import openai
import io
from PIL import Image, ImageTk

# create the main window
window = Tk()
window.geometry("1920x1080")


# set up the OpenAI API key and initialize a message list
openai.api_key = 'Enter your OpenAI key'
messages = [ {"role": "system", "content":
              "You are a intelligent assistant."} ]

# set up the MapQuest API key and other variables
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "LiK0g4cAuVKdQX7nkNGbVCFd4XIjKzNT"
good = 1;
Starting=StringVar()
global start, url, dist, json_data, dest
dist=None
Destination=StringVar()

# set up the frames for the various UI elements
frame1 = Frame(window)
frame1.pack(side='top', pady=30)
frame2 = Frame(window)
frame2.pack(side='top', pady=20)
frame3 = Frame(window)
frame3.pack(side='top', pady=15)
frame4 = Frame(window)
frame6 = Frame(window)
frame6.pack(side='top')
frame4.pack(side='top', pady=15)
frame5 = Frame(window)
frame5.pack(side='top', pady=10)

# set up the three text boxes for displaying information
msg1 = Text(frame4, height=30, width=55)
msg1.pack(side="left", expand=True, padx=20)
msg2 = Text(frame4, height=30, width=55)
msg2.pack(side="left", expand=True, padx=20)
msg3 = Text(frame4, height=30, width=55)
msg3.pack(side="left", expand=True, padx=20)

# define a function to search for directions using the MapQuest API
def search():
    msg1.delete('1.0', END)
    msg2.delete('1.0', END)
    msg3.delete('1.0', END)

    # get the starting location and destination from the entry boxes
    global json_data, good, dest, start, url
    start = Starting.get()
    dest = Destination.get()

    # build the URL for the MapQuest API
    url = main_api + urllib.parse.urlencode({"key": key, "from": start, "to": dest})

    # make a request to the API and get the JSON data
    json_data = requests.get(url).json()

    # check the status code in the JSON response
    json_status = json_data["info"]["statuscode"]
    good = json_status

    # handle various error codes returned by the API
    if json_status == 0:
        good = 0
    elif json_status == 402:
        msg1.insert(END, "********************************************** \n")
        msg1.insert(END, "Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        msg1.insert(END, "**********************************************\n")

    elif json_status == 611:
        msg1.insert(END, "********************************************** \n")
        msg1.insert(END, "Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        msg1.insert(END, "**********************************************\n")
    else:
        msg1.insert(END, "************************************************************************ \n")
        msg1.insert(END, "For Staus Code: " + str(json_status) + "; Refer to:")
        msg1.insert(END, "https://developer.mapquest.com/documentation/directions-api/status-codes")
        msg1.insert(END, "************************************************************************\n")

# Function to print the results from the Mapquest JSON to the first message box
def directions():
    global json_data,good,dest,start, dist
    dist = float("{:.2f}".format((json_data["route"]["distance"]) * 1.61))
    print(("{:.2f}".format((json_data["route"]["distance"]) * 1.61)))
    if good == 0:
        msg1.insert(END, "Directions from " + start + " to " + dest + " \n")
        msg1.insert(END, "Trip Duration: " + (json_data["route"]["formattedTime"]) + " \n")
        msg1.insert(END, "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"]) * 1.61)) + " \n")
        msg1.insert(END, "============================================= \n")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            msg1.insert(END, "- " + (each["narrative"]) + " (" + str(
                "{:.2f}".format((each["distance"]) * 1.61) + " km)") + " \n")


# Function to print the hotel information acquired from chatgpt
def hotels():
    message = "Give me 5 best hotels in " + dest + "and do not show anything in the response except the list of hotels."
    if message:
        messages.append(
            {"role": "user", "content": message}, )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    msg2.insert(END, f" {reply}")
    messages.append({"role": "assistant", "content": reply})


# Function to print the gas station information acquired from chatgpt
def gas():
    global dest,start
    message = "Give me 10 gas stations located between" + start + " and " + dest
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    msg3.insert(END, f"{reply}")
    messages.append({"role": "assistant", "content": reply})


# buttons to run the functions separately to reduce lag
btn1 = Button(frame5, text="Reveal", command=directions)
btn1.pack(side="left", expand=True, padx=220)
btn2 = Button(frame5, text="Reveal", command=hotels)
btn2.pack(side="left", expand=True, padx=250)
btn3 = Button(frame5, text="Reveal", command=gas)
btn3.pack(side="left", expand=True, padx=220)

# title of the main window
title = Label(frame1, text="GUI MAPPING", font=("Arial", 30))
title.pack(expand=True)

# Getting the starting location and destination from the user
start1 = Label(frame2, text = "Starting location", font=("Arial", 15))
start1.pack(side="left", expand=True, padx=15)
entry1 = Entry(frame2, font=("Arial", 15), textvariable = Starting)
entry1.pack(side="left", expand=True, padx=15)
start2 = Label(frame2, text="Destination", font=("Arial", 15))
start2.pack(side="left", expand=True, padx=15)
entry2 = Entry(frame2, font=("Arial", 15), textvariable=Destination)
entry2.pack(side="right", expand=True, padx=15)

# button to run a function that takes the user input and saves it as well as determining if there are errors
btn5 = Button(frame3, text="Search", font=("Arial", 10), command=search)
btn5.pack(side="left", expand=True, padx=15)

# titles of the message boxes
label1 = Label(frame6, text = "Travel Information", font=("Arial", 20))
label2 = Label(frame6, text = "Hotels", font=("Arial", 20))
label3 = Label(frame6, text = "Gas Stations", font=("Arial", 20))
label1.pack(side="left", expand=True, padx=20)
label2.pack(side="left", expand=True, padx=300)
label3.pack(side="left", expand=True, padx=75)


# Function to display the map, needs a different url but same key
def show_map():
    global start, dest, dist

    # If distance has been measured, use one of the cases, if not use the first as default
    if dist is None:
        Z = 10
    if dist is None or dist < 50:
        Z = 10
    elif 50 < dist < 150:
        Z = 9
    elif 150 < dist < 350:
        Z = 8
    elif 350 < dist < 500:
        Z = 7
    elif 500 < dist < 1500:
        z = 5
    else:
        Z = 3
    url = "https://www.mapquestapi.com/staticmap/v5/map"
    key = "LiK0g4cAuVKdQX7nkNGbVCFd4XIjKzNT"
    params = {
        "key": key,
        "size": "600,400@2x",
        "zoom": Z,
        "start": start,
        "end": dest,
    }

    # Getting the response and creating an image based on it
    response = requests.get(url, params=params)
    img_data = Image.open(io.BytesIO(response.content))
    img = ImageTk.PhotoImage(img_data)

    # create a new window for the map
    map_window = Toplevel(window)
    map_window.title("Map")

    # add the map image to a label in the new window
    map_label = Label(map_window, image=img)
    map_label.image = img
    map_label.pack()

    # run the new window mainloop
    map_window.mainloop()


Button(frame3, text="Show Map", command=show_map).pack(side="left", expand=True, padx=15)

window.mainloop()
