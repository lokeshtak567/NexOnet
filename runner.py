import tkinter as tk
import subprocess
import webbrowser
import time
import threading

#----------------------------------------------------------------------------------------------------------------#

window=tk.Tk()
window.title("NexOnet")
window.geometry("700x500")
window.resizable(False,False)

#----------------------------------------------------------------------------------------------------------------#
# Resources 

icon1=tk.PhotoImage(master=window,file="resources/credits.png")
icon2=tk.PhotoImage(master=window,file="resources/source.png")
icon3=tk.PhotoImage(master=window,file="resources/update.png")
icon4=tk.PhotoImage(master=window,file="resources/autorun.png")
icon5=tk.PhotoImage(master=window,file="resources/start.png")
icon6=tk.PhotoImage(master=window,file="resources/logo1.png")
icon7=tk.PhotoImage(master=window,file="resources/logo2.png")
icon8=tk.PhotoImage(master=window,file="resources/background.png")


def start_fun():
    command_run=subprocess.run("python wifiexploit.py")
    
    
    


def autorun_fun():
    pass

def credits_fun():
    credits = tk.Toplevel(window)
    credits.title("Credits")
    credits.geometry("320x340")
    credits.resizable(False, False)
    icon9=tk.PhotoImage(master=credits,file="resources/credits_screen.png")
    frame=tk.Frame(credits)
    frame.pack(fill=tk.BOTH,expand=False)
    credit_screen=tk.Label(frame,image=icon9,bg='black').pack(fill=tk.BOTH,expand=True)
    credits.mainloop()

def sources_fun():
    
    urls=[
        "https://www.linkedin.com/in/lokesh-tak-764b33321",
        "https://www.linkedin.com/in/vaishnavi-sharma-6465a2269",
        "https://www.linkedin.com/in/rudra-sharma-714a7b259",
        "http://www.linkedin.com/in/atharva-karamudi",
    ]

    webbrowser.open(urls[0])
    time.sleep(1)
    for url in urls[1:]:
        webbrowser.open_new_tab(url)

def update_fun():
    pass

def mainscreen():

    # Frames
    mmframe=tk.Frame(window)
    mmframe.pack(fill=tk.BOTH,expand=False)

    # Labels
    background_label=tk.Label(mmframe,image=icon8,bg='black').pack(fill=tk.BOTH,expand=True)
    logo1_label=tk.Label(mmframe,image=icon6,bg='black').place(x=4,y=0)
    logo2_label=tk.Label(mmframe,image=icon7,bg='black').place(x=100,y=155)

    # Buttons
    credits_but=tk.Button(mmframe,image=icon1,bg="black",fg="black",command=credits_fun).place(x=280,y=1)
    source_but=tk.Button(mmframe,image=icon2,bg="black",fg="black",command=sources_fun).place(x=410,y=1)
    update_but=tk.Button(mmframe,image=icon3,bg="black",fg="black",command=update_fun).place(x=570,y=1)
    autorun_but=tk.Button(mmframe,image=icon4,bg="black",fg="black",command=autorun_fun).place(x=0,y=469) 
    start_but=tk.Button(mmframe,image=icon5,bg="black",fg="black",command=start_fun).place(x=350,y=469)   
    
    

mainscreen()


window.mainloop()