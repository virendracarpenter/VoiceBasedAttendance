import pandas as pd
import pyttsx3
import speech_recognition as sr
from tkinter import *

r = sr.Recognizer()
engine = pyttsx3.init()

windows = Tk()
windows.geometry("1600x900")
windows.title("Voice Based Attendence System")
lable7 = Label(text="Voice Based Attendence System", foreground="gray", padx=10, pady=10, font=("Calibri", 35, "bold"))
lable7.pack()

lable8 = Label(windows, text="    Instructions    ", font=("Algerian", 20), foreground="gray22")
lable8.place(x=100, y=125)


s = "1- Press the mic icon to start taking attendence.\n       2- To add a new student click \"Add Student\" button"
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
            df = pd.read_csv(r'attendence.csv')
            df2 = pd.DataFrame({'Enrollment Number': [enroll], 'SE Number': [se], 'Name': [name], 'Status': [state]})
            df = pd.concat([df, df2], ignore_index=True, axis=0)
            df.to_csv("attendence.csv", index=False)

            df = pd.read_csv(r'attendence.csv')
            df1 = df.loc[:, df.columns != "Index Number"]
            sorted_df = df1.sort_values(by=["Name"], ascending=True)
            sorted_df.to_csv("attendence.csv", index=False)

            lable6 = Label(windows, text="Added Successfully")
            lable6.place(x=350, y=315)

        else:
            lable6 = Label(windows, text="Fill Entries")
            lable6.place(x=350, y=315)

    def print():
        windows = Tk()
        windows.geometry("800x450")
        windows.resizable(False, False)
        windows.title("Attendence Sheet")

        text3 = Text(windows, width=70, height=25)
        text3.pack()
        with open("attendence.csv", "r") as f:
            data = f.read()
            text3.insert("1.0", data)

    def remove():
        df = pd.read_csv(r'attendence.csv')
        df.set_index('Enrollment Number', inplace=True)
        df.head()
        en = entry1.get()
        df.drop(en, axis=1, inplace=False)
        df.to_csv("attendence.csv", index=False)
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
    #n = int(input("How many student do you want to add: "))
    #for x in range(n):
        #print("~~~~~~~~~~~~~Student ", x + 1, " Info~~~~~~~~~~~~~")
        #enroll = input("Enrollment No.: ")
        #se = input("SE No.: ")
        #name = input("Name: ")
        #state = input("Status: ")
        #df = pd.read_csv(r'attendence.csv')
        #df2 = pd.DataFrame({'Enrollment Number': [enroll], 'SE Number': [se], 'Name': [name], 'Status': [state]})
        #df = pd.concat([df, df2], ignore_index=True, axis=0)
        #df.to_csv("attendence.csv", index=False)

        #df = pd.read_csv(r'attendence.csv')
        #df1 = df.loc[:, df.columns != "Index Number"]
        #sorted_df = df1.sort_values(by=["Name"], ascending=True)
        #sorted_df.to_csv("attendence.csv", index=False)

#    df = pd.read_csv(r'attendence.csv')
#    df.reset_index(level=0, inplace=True)
#    df.to_csv("attendence.csv", index=False)

def start_attendence():
    count = 0
    df = pd.read_csv(r'attendence.csv')
    enroll = df['SE Number'].tolist()
    enrollno = df['Enrollment Number'].tolist()
    df['Status'] = 0
    df.to_csv('attendence.csv', index=False)

    for i in range(len(enroll)):
        engine.setProperty("rate", 180)
        engine.say("Enrollment number")
        engine.setProperty("rate", 150)
        engine.say(enroll[i])
        engine.runAndWait()
        k = True
        attempt = 0

        while (k and attempt < 3):
            try:

                with sr.Microphone() as source:

                    engine.setProperty("rate", 120)
                    engine.say("Speak Now")
                    engine.runAndWait()

                    text2.insert(END,"\nRecognizing..."+enrollno[i]+"\n")

                    #print("Recognizing...", end='  ')
                    #print(enrollno[i])

                    audio_data = r.record(source, duration=3)
                    text1 = r.recognize_google(audio_data)

                    text2.insert(END,text1)
                    #lable1 = Label(text=text1)
                    #lable1.pack()
                    #print(text)

                    if "present" in text1 or "yes" in text1:
                        df.loc[i, 'Status'] = 1
                        df.to_csv("attendence.csv", index=False)
                        k = False
                        count += 1
                        text2.insert(END,"\nAttendence Marked.\n")
                        #lable6 = Label(text = "Attendence Marked.")
                        #lable6.pack()
                    elif "absent" in text1 or "no" in text1:
                        # df.loc[i, 'Status'] = 0
                        k = False
                    else:
                        attempt += 1
                        tot1 = str(3-attempt)
                        text2.insert(END,"\nAttempt Left" + tot1)
                        #lable2 = Label(text="Attempt Left" + 3 - attempt)
                        #lable2.pack()
                        #print("Attempt Left", 3 - attempt)
            except sr.RequestError as e:

                text2.insert(END,"\nCould not request results\nInternet Connection Slow; {0}".format(e))
                #lable3 = Label(text="Could not request results\nInternet Connection Slow; {0}".format(e))
                #lable3.pack()
                #print("Could not request results\nInternet Connection Slow; {0}".format(e))

            except sr.UnknownValueError:
                attempt += 1
                if attempt < 3:
                    tot3 = str(3-attempt)
                    text2.insert(END,"\nTry Again\nAttempt Left"+ tot3)
                    #lable4 = Label(text="Try Again\nAttempt Left"+ 3 - attempt)
                    #lable4.pack()
                    #print("Try Again\nAttempt Left", 3 - attempt)

    tot = str(count)
    text2.insert(END,"\nNumbers of students present = "+ tot)
   # lable5 = Label(text="Numbers of students present = "+ tot)
    #lable5.pack()
    #print("Numbers of students present = ", count)


button = Button(image=pic, width=200, height=210, borderwidth=0, command= start_attendence)
button.place(x=150, y=350)
button1 = Button(text="Add/Remove Students", width=20, height=5, borderwidth=10, command= add_student)
button1.place(x=165, y=600)
text2 = Text(windows, width=100,height=40)
text2.place(x=600, y=100)

windows.mainloop()

