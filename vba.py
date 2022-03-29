from gtts import gTTS 
import speech_recognition as sr
import mysql.connector
#from playsound import playsound # uncomment to use in Windows
import os

# Path /home/virendra/Projects/python/project-vba/
r = sr.Recognizer()
path = "hello.mp3"

def speak(input):
    myobj = gTTS(text=input, lang='en', slow=False)
    
    # Saving the converted audio in a mp3 file named
    save = path
    myobj.save(save)

    # Uncomment for Windowse
    # playsound()

    #For linux
    os.system("mpg123 " + save)

def attandance(input):
    print('Input String : ' + input)

    present = False

    if "present" or "yes" in input.split():
        #speak('Student is Prensent')
        present = True
        print("present")
        print(present)
    else:        
        print(present)
        print("Absent")

def getInput():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Recognizing...")
        audio = r.record(source, duration = 5)
        print("done")
    try:
        
        MyText = r.recognize_google(audio)
        MyText = MyText.lower()
        #print("Did you say " + MyText)
        
        attandance(MyText)

        #return MyText

    # except sr.RequestError as e:
    #     speak("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        speak("unknown error occured")

# Runner code

getInput()

#details

# get name of the  student from db

# put present OR absent in repective coloumn

# next name


# dataBase = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="123qwe1q2w3e",
# )

# print(dataBase)

 
# # preparing a cursor object
# cursorObject = dataBase.cursor()

# # creating database
# cursorObject.execute("CREATE DATABASE studentRecord")

# # creating table
# studentRecord = """CREATE TABLE STUDENT (
#                    NAME  VARCHAR(20) NOT NULL,
#                    BRANCH VARCHAR(50),
#                    ROLL INT NOT NULL,
#                    SECTION VARCHAR(5),
#                    AGE INT
#                    )"""
  
# # table created
# cursorObject.execute(studentRecord)

# # disconnecting from server
# dataBase.close()