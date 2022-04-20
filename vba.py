import pandas as pd
import pyttsx3
import speech_recognition as sr


r = sr.Recognizer()
engine = pyttsx3.init()


def take_attendence():
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

                    print("Recognizing...", end='  ')
                    print(enrollno[i])

                    audio_data = r.record(source, duration=3)
                    text = r.recognize_google(audio_data)
                    print(text)

                    if text == "present" or text == "yes":
                        df.loc[i, 'Status'] = 1
                        df.to_csv("attendence.csv", index=False)
                        k = False
                        count += 1
                    elif text == "absent" or text == "no":
                        # df.loc[i, 'Status'] = 0
                        k = False
                    else:
                        attempt += 1
                        print("Attempt Left", 3 - attempt)
            except sr.RequestError as e:
                print("Could not request results\nInternet Connection Slow; {0}".format(e))

            except sr.UnknownValueError:
                attempt += 1
                if attempt < 3:
                    print("Try Again\nAttempt Left", 3 - attempt)
    print("Numbers of students present = ", count)



def add_new():
    n = int(input("How many student do you want to add: "))
    for x in range(n):
        print("~~~~~~~~~~~~~Student ",x+1," Info~~~~~~~~~~~~~")
        enroll = input("Enrollment No.: ")
        se = input("SE No.: ")
        name = input("Name: ")
        state = input("Status: ")
        df = pd.read_csv(r'attendence.csv')
        df2 = pd.DataFrame({'Enrollment Number': [enroll], 'SE Number': [se], 'Name': [name], 'Status': [state]})
        df = pd.concat([df, df2], ignore_index=True, axis=0)
        df.to_csv("attendence.csv", index=False)

        df = pd.read_csv(r'attendence.csv')
        df1 = df.loc[:, df.columns != "Index Number"]
        sorted_df = df1.sort_values(by=["Name"], ascending=True)
        sorted_df.to_csv("attendence.csv", index=False)

    df = pd.read_csv(r'attendence.csv')
    df.reset_index(level=0, inplace=True)
    df.to_csv("attendence.csv", index=False)


while(1):
    st = int(input("\n\n\n[Type 1 for Add new Student]    AND    [Type 2 for Start Attendance]    AND    [Any Other Number For TErminate Program].\n ===> "))
    if st == 1:
        print("\n\n============Adding A New Student================\n\n")
        add_new()

    elif st == 2:
        print("\n\n============Start Taking Attendance================\n\n")
        take_attendence()
    else:
        exit()