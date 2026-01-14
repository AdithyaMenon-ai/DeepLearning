import pyttsx3

txt_sp = pyttsx3.init()

f_voice = txt_sp.getProperty('voices')
txt_sp.setProperty('voice', f_voice[1].id)

txt_sp.setProperty('rate', 170)  
txt_sp.setProperty('volume', 1.0)

text = input("Enter your text: ")
txt_sp.say(text)
txt_sp.runAndWait()
