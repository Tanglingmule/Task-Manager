#libraries
import tkinter as tk
from PIL import ImageTk, Image
from datetime import datetime

#############################################################PY################################################# 
format = "%d/%m/%Y"

#commands
def validate_date_format(entryOne):
    while True:
        try:
            datetime.strptime(entryOne,format)
        except ValueError:
            #print(f"Invalid Date Format. Please use {format}")
            return False
        return True

def update_time_label():
    current_time = datetime.now().strftime("%H:%M:%S")
    timeLabel.config(text=current_time)
    mainWindow.after(1000, update_time_label)  # Schedule the next update in 1 second (1000 milliseconds)

def errorMessage(message):
    top = tk.Toplevel(None)
    top.attributes('-topmost', True)
    top.overrideredirect(True) 
    bg_image = Image.open("koiPopWide.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(top, image=bg_photo)
    bg_label.place(x=0, y=0)

    # Get the screen width and height
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    # Calculate the position for the window to be centered
    x = (screen_width - 750) // 2
    y = (screen_height - 350) // 2
    top.geometry(f"750x350+{x}+{y}")

    top.title("Error")
   
    label=tk.Label(top, text=message)  #Puts each task on its own line
    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    buttonOne = tk.Button(top, text="Close Window", width=25, command=top.destroy, fg="red")
    buttonOne.place(relx=0.1, rely=0.1)

    top.mainloop()

def popUp(title, message):
    top = tk.Toplevel(None)
    top.attributes('-topmost', True)
    top.overrideredirect(True) 
    bg_image = Image.open("koiPopWide.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(top, image=bg_photo)
    bg_label.place(x=0, y=0)

    # Get the screen width and height
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    # Calculate the position for the window to be centered
    x = (screen_width - 750) // 2
    y = (screen_height - 350) // 2
    top.geometry(f"750x350+{x}+{y}")
    top.title(title)
  

    label = tk.Label(top, text=message, bg="#FAF4F4")
    label.place(relx=0.2, rely=0.2, anchor=tk.CENTER)

    buttonOne = tk.Button(top, text="Close Window", width=25, command=top.destroy, fg="red")
    buttonOne.place(relx=0.1, rely=0.9)
    top.mainloop()

def searchTask(entryOne, entryTwo):
    file=open("database","r")
    data=file.read()
    tasks=data.split("\n")
    file.close()
    keyword = entryOne.get().strip() + entryTwo.get().strip()  # Strip whitespace from search term
    
    found_tasks = []

    for task in tasks:
        if task:
            title, description, date = task.split('|')
            if keyword.lower() == title.strip().lower() or keyword.lower() == description.strip().lower() or keyword.lower() == date.strip().lower():  # Strip whitespace from tasks
                found_tasks.append(task)

    if found_tasks:  # if foundtasks is true/has a task inside
        print("Found tasks:")
        for task in found_tasks:
            print(task)
            popUp("Task Found",task)
            return task
    else:
        print("No matching tasks found.")
        errorMessage("No Tasks Found")
        

def deleteTaskFromFile(entryOne):
    keyword = entryOne.get().strip()  # Strip whitespace from search term
    with open("database", "r") as file:
        lines = file.readlines()

    tasksToDelete = []

    for task in lines:
        if task:
            title, description, date = task.split('|')
            if keyword.lower() == title.strip().lower():  # Strip whitespace from task title
                tasksToDelete.append(task)

    with open("database", "w") as file:
        for line in lines:
            if line not in tasksToDelete:
                file.write(line)

    if tasksToDelete:
        print("Task deleted.")
    else:
        print("No matching tasks found.")
        errorMessage("No Tasks Found")


def viewTasks():
    with open("database","r") as file:
        tasks=file.read()   
    print(tasks)
    popUp("Tasks", tasks)

def overdueTasks():
    overdueTasks=[]

    currentDate = datetime.now().strftime("%d/%m/%Y")
    currentDate = datetime.strptime(currentDate, "%d/%m/%Y")

    file=open("database","r")
    data=file.read()
    tasks=data.split("\n")
    file.close()
    for task in tasks:
        if task:
            title, description, date = task.split('|')
            if validate_date_format(date):
                task_date = datetime.strptime(date, "%d/%m/%Y")
                if task_date < currentDate:
                    overdueTasks.append(task)


    popUp("Overdue Tasks", "\n".join(overdueTasks))



def getEntry(entryOne,entryTwo="",entryThree=""):
    content = entryOne.get()
    content += "|"
    content += entryTwo.get()
    content += "|"
    content += entryThree.get()
    
    print(content)
    return(content, entryOne, entryTwo, entryThree)


def addTaskToFile(entryOne, entryTwo, entryThree):
    content, _, _, _ = getEntry(entryOne, entryTwo, entryThree)
    with open("database", "a") as file:
        file.write(content + '\n')

def updateTask(entryOne, entryTwo, entryThree, found_tasks):
      
    with open("database", "r") as file:
        lines = file.readlines()

    with open("database", "w") as file:
        for line in lines:
            if line.strip() in found_tasks:
                updated_task = entryOne + "|" + entryTwo + "|" + entryThree + "\n"
                print("Updated task:", updated_task)
                file.write(updated_task)
            else:
                file.write(line)
    popUp("Task Updated",updated_task)

def updateTaskFind(entryOne):
    file = open("database", "r")
    data = file.read()
    tasks = data.split("\n")
    file.close()
    keyword = entryOne.get().strip()  # Strip whitespace from search term

    found_tasks = []

    for task in tasks:
        if task:
            title, description, date = task.split('|')
            if keyword.lower() == title.strip().lower() or keyword.lower() == description.strip().lower() or keyword.lower() == date.strip():
                found_tasks.append(task)

    if found_tasks:
        title, description, date = found_tasks[0].split('|')
        top = tk.Toplevel(None)
        top.geometry("750x250")
        top.title("Update Task")
        top.attributes('-topmost', True)
        tk.Label(top, text="Title").grid(row=1)
        tk.Label(top, text="Description").grid(row=2)
        tk.Label(top, text="Date").grid(row=3)
        e1 = tk.Entry(top)
        e2 = tk.Entry(top)
        e3 = tk.Entry(top)
        e1.grid(row=1, column=1)
        e2.grid(row=2, column=1)
        e3.grid(row=3, column=1)

        e1.insert(0, title)  # Insert the existing values into the Entry widgets
        e2.insert(0, description)
        e3.insert(0, date)

        updateButton = tk.Button(top, text="Update Task", command=lambda: updateTask(e1.get(), e2.get(), e3.get(), found_tasks))
        updateButton.grid(row=4, column=2)
    else:
        print("No matching tasks found.")
        errorMessage("No Tasks Found")


#########################TKINTER FORMATTING###########################
# window attributes
mainWindow=tk.Tk()      #Main selection Window
mainWindow.title("Task Manager")
mainWindow.attributes('-topmost',True)
#background image
frame = tk.Frame(mainWindow, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = ImageTk.PhotoImage(Image.open("background.jpg"))
label = tk.Label(frame, image = img)
label.pack()
#get rid of app bar
mainWindow.overrideredirect(True) 
#center window 
screen_width = mainWindow.winfo_screenwidth()   # Get the screen width and height
screen_height = mainWindow.winfo_screenheight()
x = (screen_width - 1280) // 2  # Calculate the position for the window to be centered
y = (screen_height - 720) // 2
mainWindow.geometry(f"1280x720+{x}+{y}")

def openWindowTwo():    #window for adding a new task
    windowTwo=tk.Toplevel(None)
    windowTwo.title("Task Add")
    windowTwo.geometry("600x600")
    windowTwo.attributes("-topmost", True)

   
    tk.Label(windowTwo, text="Title").grid(row=1)
    tk.Label(windowTwo, text="Description").grid(row=2)
    tk.Label(windowTwo, text="Date").grid(row=3)
    e1=tk.Entry(windowTwo)
    e2=tk.Entry(windowTwo)
    e3=tk.Entry(windowTwo)
    e1.grid(row=1,column=1)
    e2.grid(row=2,column=1)
    e3.grid(row=3,column=1)  

    def validate_and_toggle():
        if validate_date_format(e3.get()):
            if len(e1.get())==0 or len(e2.get())==0 or len(e3.get())==0:
                getButton2.config(state=tk.DISABLED)
            elif len(e1.get())==0 and len(e2.get())>0 and len(e3.get())>0:
                getButton2.config(state=tk.DISABLED)
            else:
                getButton2.config(state=tk.ACTIVE)
        else:
            getButton2.config(state=tk.DISABLED)

    getButton2=tk.Button(windowTwo, text="Add Task", command=lambda:addTaskToFile(e1,e2,e3))
    validate_and_toggle()
    e2.bind("<KeyRelease>", lambda event: validate_and_toggle())  # Add event binding
    e1.bind("<KeyRelease>", lambda event: validate_and_toggle())
    e3.bind("<KeyRelease>", lambda event: validate_and_toggle())
    getButton2.grid(row=4, column=4)


def openWindowThree():  #window for deleting a task
    windowThree=tk.Toplevel(None)
    windowThree.title("Delete Task")
    windowThree.geometry("600x600")
    windowThree.attributes("-topmost", True)

    tk.Label(windowThree, text="Enter Title: ").grid(row=1)
    e1=tk.Entry(windowThree)
    e1.grid(row=1, column=1)
    getButton2=tk.Button(windowThree, text="Delete Task", command=lambda:deleteTaskFromFile(e1))
    getButton2.grid(row=4, column=4)

   
def openWindowFour():   #window for searching for a task
    windowFour=tk.Toplevel(None)
    windowFour.title("Search For Task")
    windowFour.geometry("600x600")
    windowFour.attributes('-topmost',True)

    tk.Label(windowFour, text="Enter Title or Description: ").grid(row=1)
    e1=tk.Entry(windowFour)
    e1.grid(row=1, column=1)

    tk.Label(windowFour, text="or Date: ").grid(row=2)
    e2=tk.Entry(windowFour)
    e2.grid(row=2, column=1)
    
    # MAKES BUTTON UNPRESSABLE UNLESS CERTAIN CONDITIONS ARE MET
    def validate_and_toggle():
        if validate_date_format(e2.get()):
            if len(e1.get())>0 and len(e2.get())>0:
                getButton2.config(state=tk.DISABLED)
            else:
                getButton2.config(state=tk.ACTIVE)
        elif len(e1.get())>=1 and len(e2.get())>0:
                getButton2.config(state=tk.DISABLED)
        elif len(e1.get()) > 0:
            getButton2.config(state=tk.ACTIVE)
        elif len(e1.get())==0 and len(e2.get())==0:
            getButton2.config(state=tk.DISABLED)
        elif len(e1.get())>0 and len(e2.get())>0:
            getButton2.config(state=tk.DISABLED)
        else:
            getButton2.config(state=tk.DISABLED)

    getButton2=tk.Button(windowFour, text="Find Task", command=lambda:searchTask(e1, e2), state=tk.DISABLED)
    validate_and_toggle()
    e2.bind("<KeyRelease>", lambda event: validate_and_toggle())  # Add event binding
    e1.bind("<KeyRelease>", lambda event: validate_and_toggle())
    getButton2.grid(row=4, column=4)

   
def openWindowFive():    #window for updating a task
    windowFive=tk.Toplevel()
    windowFive.title("Update A Task")
    windowFive.geometry("600x600")
    windowFive.attributes("-topmost", True)

    tk.Label(windowFive, text="Enter Title, Description of task you want to update").grid(row=1)
    tk.Label(windowFive, text="or Date").grid(row=2)
    e1=tk.Entry(windowFive)
    e1.grid(row=1, column=1)
    e2=tk.Entry(windowFive)
    e2.grid(row=2, column=1)

    def validate_and_toggle():
        if validate_date_format(e2.get()):
            if len(e1.get())>=1 and len(e2.get())>0:
                getButton2.config(state=tk.DISABLED)
            else:
                getButton2.config(state=tk.ACTIVE)
        elif len(e1.get())>=1 and len(e2.get())>0:
                getButton2.config(state=tk.DISABLED)
        elif len(e1.get()) > 0:
            getButton2.config(state=tk.ACTIVE)
        elif len(e1.get())==0 and len(e2.get())==0:
            getButton2.config(state=tk.DISABLED)
        elif len(e1.get())>0 and len(e2.get())>0:
            getButton2.config(state=tk.DISABLED)
        else:
            getButton2.config(state=tk.DISABLED)
            
            
    getButton2=tk.Button(windowFive, text="Find Task To Update", command=lambda:updateTaskFind(e1), state=tk.DISABLED)
    validate_and_toggle()
    e2.bind("<KeyRelease>", lambda event: validate_and_toggle())  # Add event binding
    e1.bind("<KeyRelease>", lambda event: validate_and_toggle())
    getButton2.grid(row=3, column=1)




# ALL ELEMENTS ON THE MAIN WINDOW
welcome=tk.Label(mainWindow, text="Task Manager", bg="#c1c1c1", font=("Arial", 25), fg="#fc1e07")
welcome.place(relx=0.5, rely=0.03, anchor=tk.CENTER)

currentTimeLabel= tk.Label(mainWindow, text="Current Time:", bg="#c1c1c1", font=("Arial", 25), fg="#fc1e07")
currentTimeLabel.place(x=100, y= 250)
timeLabel = tk.Label(mainWindow, font=("Terminal", 50), bg="#c1c1c1", fg="#fc1e07")
timeLabel.place(x=100, y=300)

winTwo=tk.Button(mainWindow, text="Add Task", width=25, command=openWindowTwo, fg="black", activebackground="orange")
winTwo.place(x=100, y=100)

winThree=tk.Button(mainWindow, text="Delete Task", width=25, command=openWindowThree, fg="black", activebackground="orange")
winThree.place(x=300, y=100)

winFour=tk.Button(mainWindow, text="Search for a task", width=25, command=openWindowFour, fg="black", activebackground="orange")
winFour.place(x=500, y=100)

winFive=tk.Button(mainWindow, text="Update Task", width=25, command=openWindowFive, activebackground="orange")
winFive.place(x= 300, y=150)

buttonOne= tk.Button(mainWindow, text="Stop application", width=25, command=mainWindow.destroy, fg="red")
buttonOne.place(x=0, y=695)

buttonTwo= tk.Button(mainWindow, text="View Tasks", width=25, command=viewTasks, activebackground="orange")
buttonTwo.place(x=100, y=150)

buttonThree= tk.Button(mainWindow, text="Overdue Tasks", width=25, command=overdueTasks, activebackground="orange", fg="red")
buttonThree.place(x=500, y=150)

update_time_label()
mainWindow.mainloop()