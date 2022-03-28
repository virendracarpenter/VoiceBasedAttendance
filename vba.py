from gtts import gTTS 
import speech_recognition as sr

#from playsound import playsound # uncomment to use in Windows
import os 

# Path /home/virendra/Projects/python/project-vba/
path = "hello.mp3"

def speak(input):
    myobj = gTTS(text=input, lang='en', slow=False)

    # Saving the converted audio in a mp3 file named
    save = path
    myobj.save(save)
    
    # Playing the converted file
    # Uncomment for Windowse
    # playsound()

    #For linux
    os.system("mpg123 " + save)


#speak('Hello, How are you, welcome Virendra')

#Initiаlize  reсоgnizer  сlаss  (fоr  reсоgnizing  the  sрeeсh)
r = sr.Recognizer()

#while(1):    
    # Exception handling to handle
    # exceptions at the runtime
#    try:   
        # use the microphone as source for input.
        
with sr.Microphone() as source:
    
    # wait for a second to let the recognizer
    # adjust the energy threshold based on
    # the surrounding noise level
    r.adjust_for_ambient_noise(source, duration=0.2)
             
    # listens for the user's input
    #audio = r.listen(source)
    print("Recognizing...")
    audio = r.record(source, duration = 5)
    try:
            
        # Using google to recognize audio
        MyText = r.recognize_google(audio)
        MyText = MyText.lower()
            
        print("Did you say " + MyText)
        speak(MyText)
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
       print("unknown error occured")