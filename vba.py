import tkinter
from turtle import showturtle
import pandas as pd
import os
from pandasgui import show
import pyttsx3
import shutil
import datetime
import speech_recognition as sr
from tkinter import *
#from .vba import main

r = sr.Recognizer()
engine = pyttsx3.init()


# getting the timestamp in now variable
now = str(datetime.datetime.now())[:19]
now = now.replace(":","_")

# source and destination directory of attendence file
src_dir="attendence/attendence.csv"
dst_dir="attendence/"+"t3_"+str(now)+".csv"

shutil.copy(src_dir,dst_dir)

# main window gui 
windows = Tk()
windows.geometry("1600x900")
windows.title("Voice Based Attendence System")

lable7 = Label(text="Voice Based Attendence System", foreground="gray", padx=10, pady=10, font=("Calibri", 35, "bold"))
lable7.pack()

lable8 = Label(windows, text="    Instructions    ", font=("Algerian", 20), foreground="gray22")
lable8.place(x=100, y=125)

s = "1- Press the mic icon to  start taking attendence.\n       2- To add a new student click \"Add Student\" button"
lable9 = Label(text=s, font=("Times", 15))
lable9.place(x=0, y=200)
pic = PhotoImage(file="mic2.png")


def add_student():
    windows = Tk()
    windows.geometry("800x450")
    windows.resizable(False, False)
    windows.title("Add Or Remove Student")

    def add():
        enroll = entry1.get()
        se = entry2.get()
        name = entry3.get()
        state = entry4.get()


        if(enroll != "" and se != "" and name != "" and state != ""):
            df = pd.read_csv(dst_dir)
            df2 = pd.DataFrame({'Enrollment Number': [enroll], 'SE Number': [se], 'Name': [name], 'Status': [state]})
            df = pd.concat([df, df2], ignore_index=True, axis=0)
            df.to_csv(dst_dir, index=False)

            df = pd.read_csv(dst_dir)
            df1 = df.loc[:, df.columns != "Index Number"]
            sorted_df = df1.sort_values(by=["Name"], ascending=True)
            sorted_df.to_csv(dst_dir, index=False)

            lable6 = Label(windows, text="Added Successfully")
            lable6.place(x=350, y=315)

        else:
            lable6 = Label(windows, text="Fill Entries")
            lable6.place(x=350, y=315)

    def print():

        show(pd.read_csv(dst_dir))

        text3 = Text(windows, width=70, height=25)
        text3.pack()
        with open(dst_dir, "r") as f:
            data = f.read()
            text3.insert("1.0", data)

    def remove():
        df = pd.read_csv(dst_dir)
        df.set_index('Enrollment Number', inplace=True)
        df.head()
        en = entry1.get()
        df.drop(en, axis=1, inplace=False)
        df.to_csv(dst_dir, index=False)
        lable6 = Label(windows, text="Removed Successfully")
        lable6.place(x=350, y=315)

    lable1 = Label(windows, text="Add Or Remove Students", foreground="gray", padx=10, pady=10, font=("Calibri", 20, "bold"))
    lable1.pack()
    lable2 = Label(windows, text="Enrollment Number : ")
    lable2.place(x=250,y=120)
    entry1 = Entry(windows)
    entry1.place(x=400,y=120)
    lable3 = Label(windows, text="SE Number : ")
    lable3.place(x=295,y=145)
    entry2 = Entry(windows)
    entry2.place(x=400, y=145)
    lable4 = Label(windows, text="Name : ")
    lable4.place(x=322, y=170)
    entry3 = Entry(windows)
    entry3.place(x=400, y=170)
    lable5 = Label(windows, text="Status : ")
    lable5.place(x=322,y=195)
    entry4 = Entry(windows)
    entry4.place(x=400, y=195)
    button2 = Button(windows, text="Add", command=add)
    button2.place(x=325, y=275)
    button3 = Button(windows, text="Attendence Sheet", command=print)
    button3.place(x=425, y=275)
    button4 = Button(windows, text="Remove", command=remove)
    button4.place(x=365, y=275)

    windows.mainloop()

def take_attendance():
    count = 0
    df = pd.read_csv(dst_dir)
    enroll = df['SE Number'].tolist()
    enrollno = df['Enrollment Number'].tolist()
    df['Status'] = 0
    df.to_csv(dst_dir, index=False)

    for i in range(len(enroll)):
        engine.setProperty("rate", 180)
        engine.say("Enrollment number")
        engine.setProperty("rate", 150)
        engine.say(enroll[i])
        engine.runAndWait()
        k = True
        attempt = 0
        
        while (k and attempt < 2):
            try:
                with sr.Microphone() as source:

                        engine.setProperty("rate", 150)
                        engine.say("Speak Now")
                        engine.runAndWait()

                        showText.insert(END,"\n"+enrollno[i]+" - ")

                        audio_data = r.record(source, duration=3)
                        inputText = r.recognize_google(audio_data)

                        # showText.insert(END,inputText)

                        if "present" in inputText or "yes" in inputText:
                            df.loc[i, 'Status'] = 1
                            df.to_csv(dst_dir, index=False)
                            count += 1
                            showText.insert(END,"Present\n")
                            k = False
                        elif "absent" in inputText or "no" in inputText:
                            showText.insert(END,"Absent\n")
                            k = False
                        else:
                            attempt += 1
                            # tot1 = str(2-attempt)
                            # showText.insert(END,"\nAttempt Left" + tot1)
                            
            except sr.RequestError as e:
                tkinter.messagebox.showwarning(title='warning', message="Could not request results\nInternet Connection Slow")

            except sr.UnknownValueError:
                attempt += 1
                if attempt == 1:
                            showText.insert(END,"Absent\n")
                # if attempt < 2:
                    # tot3 = str(2-attempt)
                    # showText.insert(END,"\nTry Again\nAttempt Left"+ tot3)
    tot = str(count)
    showText.insert(END,"\nNumbers of students present = "+ tot)

startAttendanceButton = Button(image=pic, width=200, height=210, borderwidth=0, command= take_attendance)
startAttendanceButton.place(x=150, y=350)

addStudentButton = Button(text="Add/Remove Students", width=20, height=5, borderwidth=10, command= add_student)
addStudentButton.place(x=165, y=600)
showText = Text(windows, width=100,height=40)
showText.place(x=600, y=100)

windows.mainloop()