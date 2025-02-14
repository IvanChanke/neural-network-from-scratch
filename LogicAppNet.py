import tkinter as tk
import os
from annotations import *
from PIL import Image, ImageTk
from time import strftime
import pickle
import ptron as pt
import tdata as dt
import time

# GLOBAL VARIABLES

model = None # Current model programmed in
model_name = None
learning_rate = 0
training_data = None # Training data depends on the model selected
mainfont = ('calibri', '12')


class DigitsRecognizerApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('220x370')
        self.resizable(width=False, height=False)

        self.frames = {}  # A dictionary of pages
        self.frames['Home'] = Page(self)
        self.frames['Query'] = Page(self)
        self.frames['Learning'] = Page(self)
        self.frames['Load'] = Page(self)
        self.frames['New'] = Page(self)

        self.show_frame('Home')

    def show_frame(self, page):

        self.frames[page].tkraise()
        self.title('{}'.format(page))


class Page(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.place(relheight=1, relwidth=1)


# ---GUI---

def select_number():
    selected_number = num_entry.get()
    if selected_number not in [str(i) for i in range(0, 10)]:
        num_entry.delete(0, tk.END)
        num_entry.insert(tk.END, 'X')
    else:
        num_entry.delete(0, tk.END)
        num_entry.insert(tk.END, 'OK')
        selected_number = int(selected_number)

        return selected_number

def update_time():
    clock_home.config(text=strftime("%H:%M:%S"))
    clock_home.after(1000, update_time)

# ---MODEL-FILE-MANAGEMENT---

def load_model():

    global model
    global model_name

    file = str(file_name_entry.get())
    try:
        f = open(file, 'rb')
        model = pickle.load(f)
        model_name = file
        f.close()
        status_text.set(model_name)
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(tk.END, 'Model loaded')
        mse_text.set(model.mse)
        print('+---------------------------------------------+')
        print('MODEL {} WAS LOADED.'.format(file))
        print('+---------------------------------------------+')
    except:
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(tk.END, 'No such file')

def initialize_model(preset):

    global model
    global training_data

    models = {
        'XOR3' : pt.Network((3, 2, 1)),
        'XOR2' : pt.Network((2, 2, 1)),
        'AND3' : pt.Network((3, 2, 1)),
        'OR3' : pt.Network((3, 2, 1))
    }
    training_data = dt.data[preset]

    model = models[preset]
    print('+---------------------------------------------+')
    print('|{: ^45}|'.format('A MODEL WAS INITIALIZED'))
    print('+---------------------------------------------+')
    status_text.set('Unsaved {}'.format(preset))
    mse_text.set(model.mse)
    query_buttons = [goquery_h, goquery_l]
    for button in query_buttons:
        button['state'] = 'normal'
    send_buttons = [
        send_1_0_0, send_1_0_1, send_1_1_0, send_1_1_1
    ]
    if preset == 'XOR2':
        for button in send_buttons:
            button['state'] = 'disabled'
    else:
        for button in send_buttons:
            button['state'] = 'normal'

def send(signal):
    try:
        model.ask(signal)
    except:
        model.ask(signal[1:])

def delete_model():

    global model
    global model_name

    model = None
    status_text.set('No model loaded')
    file_name_entry.delete(0, tk.END)
    file_name_entry.insert(tk.END, 'Model deleted')
    query_buttons = [goquery_h, goquery_l]
    for button in query_buttons:
        button['state'] = 'disabled'

def save_model():

    global model

    file = str(file_name_entry.get())
    f = open(file, 'wb')
    pickle.dump(model, f)
    file_name_entry.delete(0, tk.END)
    file_name_entry.insert(tk.END, 'Model saved')
    status_text.set(file)
    f.close()
    print('+---------------------------------------------+')
    print('|{: ^45}|'.format('MODEL SUCCESSFULLY SAVED'))
    print('+---------------------------------------------+')


# ---TRAINING-QUERY-CONTROL---

def set_lrate():

    global learning_rate

    learning_rate = float(learning_rate_box_l.get())
    print('+---------------------------------------------+')
    print('|{: ^40}{:.3f}|'.format('LEARNING RATE SET TO', learning_rate))
    print('+---------------------------------------------+')
    rate_text.set(learning_rate)

def learn():

    global model

    if (model != None):
        iterations = int(iterations_entry.get())
        for i in range(iterations):
            model.learning_iteration(training_data, learning_rate)
        learning_status_text.set('Model\nis\nready')
        mse_text.set('{:.3f}'.format(model.mse))
    else:
        learning_status_text.set('No\nmodel\ndetected')
        iterations_entry.delete(0, tk.END)
        iterations_entry.insert(tk.END, 'X')

def reset_model():

    global model

    rate_text.set(0)
    mse_text.set(None)
    model = pt.Network(model.structure)
    print('+---------------------------------------------+')
    print('|{: ^45}|'.format('THE MODEL WAS RESET'))
    print('+---------------------------------------------+')

def clear_screen():
    os.system('cls')
    show_greeting()

#---GUI--CODE--STARTS--HERE---
app = DigitsRecognizerApp()
show_greeting()
# STRINGVARS
status_text = tk.StringVar()
status_text.set('No loaded model')
mse_text = tk.StringVar()
mse_text.set(None)
rate_text = tk.StringVar()
rate_text.set(0)
learning_status_text = tk.StringVar()
learning_status_text.set('Model\nis\nready')

# ---HOME---
working = app.frames['Home']
# Buttons
golearn_h = tk.Button(
    working, text ='Train', font = mainfont, width = 7,
    command = lambda: app.show_frame('Learning')
)
goquery_h = tk.Button(
    working, text = 'Query', font = mainfont, width = 5,
    command = lambda: app.show_frame('Query')
)
exit_h = tk.Button(
    working, text = 'Exit', font = mainfont,
    width = 7, command = app.quit
)
load = tk.Button(
    working, text = 'Files', font = mainfont,
    width = 7, command = lambda: app.show_frame('Load')
)
initialize = tk.Button(
    working, text = 'New Model', font = mainfont,
    width = 9, command = lambda: app.show_frame('New')
)
guide = tk.Button(
    working, text = 'Print Guide', font = mainfont,
    width = 18, command = lambda: print_guide()
)
clear = tk.Button(
    working, text = 'Clear Screen', font = mainfont,
    width = 18, command = lambda: clear_screen()
)
clear.place(anchor = 'c', relx = 0.5, rely = 0.72)
guide.place(anchor = 'c', relx = 0.5, rely = 0.62)
load.place(anchor = 'c', relx = 0.3, rely = 0.52)
initialize.place(anchor = 'c', relx = 0.65, rely = 0.52)
golearn_h.place(anchor = 'c', relx = 0.23, rely = 0.9)
goquery_h.place(anchor = 'c', relx = 0.5, rely = 0.9)
goquery_h['state'] = 'disabled'
exit_h.place(anchor = 'c', relx = 0.77, rely = 0.9)

# Labels
clock_home = tk.Label(
    working, text = strftime('%H:%M:%S'),
    font = ('calibri', '16')
)
update_time()
title_text = tk.Label(
    working, font = ('calibri', '14'),
    text = 'NeuralNet Project'
)
copyright_text = tk.Label(
    working, font = ('calibri', '10'),
    text = '© Ivan Chanke'
)

copyright_text.place(anchor = 'n', relx = 0.5, rely = 0.12)
title_text.place(anchor = 'n', relx = 0.5, rely = 0.05)
clock_home.place(anchor ='c', relx = 0.5, rely = 0.25)
clock_home.after(100, update_time)

# Texts and Entries
status_box = tk.Label(
    working, height = 3, width = 25, textvariable = status_text,
    font = mainfont
)

status_box.place(anchor = 'c', relx = 0.5, rely = 0.4)



#---NEW---
working = app.frames['New']
# Buttons
done_new = tk.Button(
    working, text = 'Done', font = mainfont,
    width = 7, command = lambda: app.show_frame('Home')
)
xor3_button = tk.Button(
    working, text = 'XOR3', font = mainfont,
    width = 15, command = lambda: initialize_model('XOR3')
)
xor2_button = tk.Button(
    working, text = 'XOR2', font = mainfont,
    width = 15, command = lambda: initialize_model('XOR2')
)
and3_button = tk.Button(
    working, text = 'AND3', font = mainfont,
    width = 15, command = lambda: initialize_model('AND3')
)
or3_button = tk.Button(
    working, text = 'OR3', font = mainfont,
    width = 15, command = lambda: initialize_model('OR3')
)

xor3_button.place(anchor = 'c', relx = 0.5, rely = 0.4)
xor2_button.place(anchor = 'c', relx = 0.5, rely = 0.5)
and3_button.place(anchor = 'c', relx = 0.5, rely = 0.6)
or3_button.place(anchor = 'c', relx = 0.5, rely = 0.7)
done_new.place(anchor = 'c', relx = 0.77, rely = 0.9)

# Labels, Text and Entries

instructions_new_label = tk.Label(
    working, text = 'To create a new model,\n select a configuration \n \
    and press "Create Model"\n To save, go to "Load" page',
    font = mainfont
)

instructions_new_label.place(anchor = 'c', relx = 0.5, rely = 0.15)




#---LOAD---
working = app.frames['Load']

# Buttons
done_load = tk.Button(
    working, text = 'Done', font = mainfont,
    width = 7, command = lambda: app.show_frame('Home')
)
get_model = tk.Button(
    working, text = 'Get Model', font = mainfont,
    width = 20, command = lambda: load_model()
)
delete_model_button = tk.Button(
    working, text = 'Delete Model', font = mainfont,
    width = 20, command = lambda: delete_model()
)
save_model_button = tk.Button(
    working, text = 'Save Model', font = mainfont,
    width = 20, command = lambda: save_model()
)
save_model_button.place(anchor = 'c', relx = 0.5, rely = 0.69)
delete_model_button.place(anchor = 'c', relx = 0.5, rely = 0.79)
get_model.place(anchor = 'c', relx = 0.5, rely = 0.59)
done_load.place(anchor = 'c', relx = 0.77, rely = 0.9)

# Labels, Text and Entries
enter_path_to_model_label = tk.Label(
    working, text = 'Enter file name:',
    font = mainfont
)
instructions_load_label = tk.Label(
    working, text = 'To load a model, \n enter the file name below \n \
    and press "Get Model"\n To save,\n enter the name and press \n "Save Model"',
    font = mainfont
)
file_name_entry = tk.Entry(
    working, font = mainfont, width = 20,
)

file_name_entry.place(anchor = 'c', relx = 0.5, rely = 0.49)
instructions_load_label.place(anchor = 'c', relx = 0.5, rely = 0.19)
enter_path_to_model_label.place(anchor = 'c', relx = 0.5, rely = 0.39)

#---QUERY---
working = app.frames['Query']

# Buttons
#reset_accuracy_q = tk.Button(
    #working, text = 'Reset accuracy', font = mainfont,
    #width = 22
#)
# selectnum_q = tk.Button(
#     working, text = 'Select number', font = mainfont,
#     command = lambda: select_number()
# )
send_0_0_0 = tk.Button(
    working, text = 'Send 0-0-0', font = mainfont, width = 18,
    command = lambda: send([0, 0, 0])
)
send_0_0_1 = tk.Button(
    working, text = 'Send 0-0-1', font = mainfont, width = 18,
    command = lambda: send([0, 0, 1])
)
send_0_1_0 = tk.Button(
    working, text = 'Send 0-1-0', font = mainfont, width = 18,
    command = lambda: send([0, 1, 0])
)
send_0_1_1 = tk.Button(
    working, text = 'Send 0-1-1', font = mainfont, width = 18,
    command = lambda: send([0, 1, 1])
)
send_1_0_0 = tk.Button(
    working, text = 'Send 1-0-0', font = mainfont, width = 18,
    command = lambda: send([1, 0, 0])
)
send_1_0_1 = tk.Button(
    working, text = 'Send 1-0-1', font = mainfont, width = 18,
    command = lambda: send([1, 0, 1])
)
send_1_1_0 = tk.Button(
    working, text = 'Send 1-1-0', font = mainfont, width = 18,
    command = lambda: send([1, 1, 0])
)
send_1_1_1 = tk.Button(
    working, text = 'Send 1-1-1', font = mainfont, width = 18,
    command = lambda: send([1, 1, 1])
)
golearn_q = tk.Button(
    working, text = 'Train', font = mainfont, width = 7,
    command = lambda: app.show_frame('Learning')
)
gohome_q = tk.Button(
    working, text = '⌂', font = mainfont, width = 5,
    command = lambda: app.show_frame('Home')
)
exit_q = tk.Button(
    working, text = 'Exit', font = mainfont,
    width = 7, command = app.quit
)
# next_instance_q = tk.Button(
#     working, text = 'Next instance (random)', font = mainfont,
#     width = 22
# )

#reset_accuracy_q.place(anchor = 'c', relx = 0.5, rely = 0.775)
#selectnum_q.place(anchor = 'c', relx = 0.685, rely = 0.660)
send_0_0_0.place(anchor = 'c', relx = 0.5, rely = 0.07)
send_0_0_1.place(anchor = 'c', relx = 0.5, rely = 0.17)
send_0_1_0.place(anchor = 'c', relx = 0.5, rely = 0.27)
send_0_1_1.place(anchor = 'c', relx = 0.5, rely = 0.37)
send_1_0_0.place(anchor = 'c', relx = 0.5, rely = 0.47)
send_1_0_1.place(anchor = 'c', relx = 0.5, rely = 0.57)
send_1_1_0.place(anchor = 'c', relx = 0.5, rely = 0.67)
send_1_1_1.place(anchor = 'c', relx = 0.5, rely = 0.77)
golearn_q.place(anchor = 'c', relx = 0.23, rely = 0.9)
gohome_q.place(anchor = 'c', relx = 0.5, rely = 0.9)
exit_q.place(anchor = 'c', relx = 0.77, rely = 0.9)
#next_instance_q.place(anchor = 'c', relx = 0.5, rely = 0.550)

# Label
# num_pic_label = tk.Label(
#     working, image = mnist_num_pic,
# )
# mode_text_q = tk.Label(
#     working, text = 'Query Control',
#     font = mainfont
# )
# accuracy_text = tk.Label(
#     working, text = '• Current accuracy:',
#     font = mainfont
# )
# digit_text = tk.Label(
#     working, text = '• Digit considered:', font = mainfont
# )
# digpic_text = tk.Label(
#     working, text = '• Digit picture:', font = mainfont
# )
#
# response_text = tk.Label(
#     working, text = "• Network response:",
#     font = mainfont
# )"

# num_pic_label.place(relx = 0.71, rely = 0.09)
# mode_text_q.place(relx = 0.02, rely = 0.005)
# accuracy_text.place(relx = 0.02, rely = 0.2)
# digit_text.place(relx = 0.02, rely = 0.3)
# digpic_text.place(relx = 0.02, rely = 0.1)
# response_text.place(relx = 0.02, rely = 0.4)

# Text and entries
# accuracy_box = tk.Text(
#     working, height = 1, width = 5,
#     font = mainfont, insertontime = 0
# )
# digit_considered_box = tk.Text(
#     working, height = 1, width = 5,
#     font = mainfont, insertontime = 0
# )
# response_box = tk.Text(
#     working, height = 1, width = 5,
#      font = mainfont, insertontime = 0
# )
# num_entry = tk.Entry(
#     working, font = mainfont, width = 5,
# )
#
# accuracy_box.place(relx = 0.72, rely = 0.205)
# accuracy_box.insert(tk.END, '100%')
# digit_considered_box.place(relx = 0.72, rely = 0.305)
# digit_considered_box.insert(tk.END, '07')
# response_box.place(relx = 0.72, rely = 0.405)
# response_box.insert(tk.END, '07')
# num_entry.place(anchor = 'se', relx = 0.35, rely = 0.694)"""


#---LEARNING---
working = app.frames['Learning']

#Buttons
update_rate_l = tk.Button(
    working, text = 'Set learning rate', width = 13,
    font = mainfont, command = lambda: set_lrate()
    )
reset_l = tk.Button(
    working, text = 'Reset', width = 7, font = mainfont,
    command = lambda: reset_model()
)
start_l = tk.Button(
    working, text = 'Start', width = 7, font = mainfont,
    command = lambda: learn()
)
stop_l = tk.Button(
    working, text = 'Stop', width = 7, font = mainfont,
    command = lambda: stop_training()
)
goquery_l = tk.Button(
    working, text = 'Query', font = mainfont,
    width = 7, command = lambda: app.show_frame('Query')
)
exit_l = tk.Button(
    working, text = 'Exit', font = mainfont,
    width = 7, command = app.quit
)
gohome_l = tk.Button(
    working, text = '⌂', font = mainfont, width = 5,
    command = lambda: app.show_frame('Home')
)

update_rate_l.place(anchor = 'se', relx = 0.92, rely = 0.8)
reset_l.place(anchor = 'c', relx = 0.23, rely = 0.6)
start_l.place(anchor = 'c', relx = 0.23, rely = 0.5)
goquery_l.place(anchor = 'c', relx = 0.23, rely = 0.9)
goquery_l['state'] = 'disabled'
gohome_l.place(anchor = 'c', relx = 0.5, rely = 0.9)
exit_l.place(anchor = 'c', relx = 0.77, rely = 0.9)

# Labels and entries
learning_info_l = tk.Label(
    working, height = 5, width = 12, font = mainfont, textvariable = learning_status_text
)
speed_box_l = tk.Label(
    working, height = 1, width = 5, font = mainfont, textvariable = rate_text
)
speed_text_l = tk.Label(
    working, text = '• Current learning rate:', font = mainfont
)
error_text_l = tk.Label(
    working, text = '• MSE value:', font = mainfont
)
error_box_l = tk.Label(
    working, height = 1, width = 5, font = mainfont, textvariable = mse_text
)
mode_text_l = tk.Label(
    working, text = "Training Control",
    font = mainfont
)
iterations_text = tk.Label(
    working, height = 1, width = 7, font = mainfont, text = 'Enter n:'
)
iterations_entry = tk.Entry(
    working, width = 5, font = mainfont
)
learning_rate_box_l = tk.Entry(
    working, font = mainfont, width = 5
)

iterations_text.place(anchor = 'c', relx = 0.23, rely = 0.32)
iterations_entry.place(anchor = 'c', relx = 0.23, rely = 0.4)
learning_rate_box_l.place(anchor = 'se', relx = 0.33, rely = 0.79)
learning_info_l.place(anchor = 'c', relx = 0.65, rely = 0.5)
error_box_l.place(relx = 0.725, rely = 0.2)
error_text_l.place(relx = 0.02, rely = 0.2)
speed_box_l.place(relx = 0.72, rely = 0.1)
speed_text_l.place(relx = 0.02, rely = 0.1)
mode_text_l.place(relx = 0.02, rely = 0.005)
learning_rate_box_l.insert(tk.END, '0')

app.mainloop()
