import tkinter as tk
from PIL import Image, ImageTk
from time import strftime
import pickle
import network_code_eng as net

# GLOBAL VARIABLES

model = None
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
        self.frames['Config'] = Page(self)
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
        num_entry.insert(tk.END, '...')
        selected_number = int(selected_number)

        return selected_number

def load_model():

    global model

    file = str(file_name_entry.get())
    try:
        f = open(file, 'rb')
        model = pickle.load(f)
        f.close()
    except:
        file_name_entry.delete(0, tk.END)
        file_name_entry.insert(tk.END, 'No such file')

def update_time():
    clock_home.config(text=strftime("%H:%M:%S"))
    clock_home.after(1000, update_time)


app = DigitsRecognizerApp()


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
configure_model = tk.Button(
    working, text = 'Configure Model', font = mainfont, width = 24,
    command = lambda: app.show_frame('Config')
)
configure_model.place(anchor = 'c', relx = 0.5, rely = 0.55)
golearn_h.place(anchor = 'c', relx = 0.23, rely = 0.9)
goquery_h.place(anchor = 'c', relx = 0.5, rely = 0.9)
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
instructions_text = tk.Label(
    working, text = 'Go to "Train" to configure the network\n\
    Go to "Query" to test the network', font = ('calibri', '10')
)

copyright_text.place(anchor = 'n', relx = 0.5, rely = 0.12)
title_text.place(anchor = 'n', relx = 0.5, rely = 0.05)
instructions_text.place(anchor = 'c', relx = 0.5, rely = 0.7)
clock_home.place(anchor ='c', relx = 0.5, rely = 0.25)
clock_home.after(100, update_time)

# Texts and Entries
status_box = tk.Text(
    working, height = 3, width = 25,
    font = mainfont, insertontime = 0
)

status_box.insert(tk.END, '{:^38}'.format('No loaded model'))
status_box.insert(tk.END, '\n\n{:}'.format('Click below to manage models'))

status_box.place(anchor = 'c', relx = 0.5, rely = 0.4)



#---CONFIGURE---
working = app.frames['Config']
# Buttons
gohome_c = tk.Button(
    working, text = 'Home', font = mainfont,
    width = 7, command = lambda: app.show_frame('Home')
)
load = tk.Button(
    working, text = 'Load Model', font = mainfont,
    width = 11, command = lambda: app.show_frame('Load')
)
initialize = tk.Button(
    working, text = 'New Model', font = mainfont,
    width = 11, command = lambda: app.show_frame('New')
)

load.place(anchor = 'c', relx = 0.73, rely = 0.41)
initialize.place(anchor = 'c', relx = 0.27, rely = 0.41)
gohome_c.place(anchor = 'c', relx = 0.77, rely = 0.9)

# Labels, Text and Entries
current_model_label = tk.Label(
    working, text = 'Current model:',
    font = mainfont
)
current_model_text = tk.Text(
    working, height = 3, width = 25,
    font = mainfont, insertontime = 0
)
current_model_text.insert(tk.END, '{}'.format('No model'))

current_model_label.place(anchor = 'c', relx = 0.5, rely = 0.05)
current_model_text.place(anchor = 'c', relx = 0.5, rely = 0.22)

#---NEW---
working = app.frames['New']
# Buttons
done_new = tk.Button(
    working, text = 'Done', font = mainfont,
    width = 7, command = lambda: app.show_frame('Config')
)

done_new.place(anchor = 'c', relx = 0.77, rely = 0.9)

#---LOAD---
working = app.frames['Load']
# Buttons
done_load = tk.Button(
    working, text = 'Done', font = mainfont,
    width = 7, command = lambda: app.show_frame('Config')
)
get_model = tk.Button(
    working, text = 'Get Model', font = mainfont,
    width = 20, command = lambda: load_model()
)
get_model.place(anchor = 'c', relx = 0.5, rely = 0.3)
done_load.place(anchor = 'c', relx = 0.77, rely = 0.9)

# Labels, Text and Entries
enter_path_to_model_label = tk.Label(
    working, text = 'Enter file name:',
    font = mainfont
)
file_name_entry = tk.Entry(
    working, font = mainfont, width = 20,
)

file_name_entry.place(anchor = 'c', relx = 0.5, rely = 0.2)
enter_path_to_model_label.place(anchor = 'c', relx = 0.5, rely = 0.1)

#---QUERY---
working = app.frames['Query']
# Buttons
reset_accuracy_q = tk.Button(
    working, text = 'Reset accuracy', font = mainfont,
    width = 22
)
selectnum_q = tk.Button(
    working, text = 'Select number', font = mainfont,
    command = lambda: select_number()
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
next_instance_q = tk.Button(
    working, text = 'Next instance (random)', font = mainfont,
    width = 22
)

reset_accuracy_q.place(anchor = 'c', relx = 0.5, rely = 0.775)
selectnum_q.place(anchor = 'c', relx = 0.685, rely = 0.660)
golearn_q.place(anchor = 'c', relx = 0.23, rely = 0.9)
gohome_q.place(anchor = 'c', relx = 0.5, rely = 0.9)
exit_q.place(anchor = 'c', relx = 0.77, rely = 0.9)
next_instance_q.place(anchor = 'c', relx = 0.5, rely = 0.550)
# Labels
mnist_num_pic = ImageTk.PhotoImage(Image.open('MNIST_number7.png'))
num_pic_label = tk.Label(
    working, image = mnist_num_pic,
)
mode_text_q = tk.Label(
    working, text = 'The Network is in query mode.',
    font = mainfont
)
accuracy_text = tk.Label(
    working, text = '• Current accuracy:',
    font = mainfont
)
digit_text = tk.Label(
    working, text = '• Digit considered:', font = mainfont
)
digpic_text = tk.Label(
    working, text = '• Digit picture:', font = mainfont
)

response_text = tk.Label(
    working, text = "• Network response:",
    font = mainfont
)

num_pic_label.place(relx = 0.71, rely = 0.09)
mode_text_q.place(relx = 0.02, rely = 0.005)
accuracy_text.place(relx = 0.02, rely = 0.2)
digit_text.place(relx = 0.02, rely = 0.3)
digpic_text.place(relx = 0.02, rely = 0.1)
response_text.place(relx = 0.02, rely = 0.4)
# Text and entries
accuracy_box = tk.Text(
    working, height = 1, width = 5,
    font = mainfont, insertontime = 0
)
digit_considered_box = tk.Text(
    working, height = 1, width = 5,
    font = mainfont, insertontime = 0
)
response_box = tk.Text(
    working, height = 1, width = 5,
     font = mainfont, insertontime = 0
)
num_entry = tk.Entry(
    working, font = mainfont, width = 5,
)

accuracy_box.place(relx = 0.72, rely = 0.205)
accuracy_box.insert(tk.END, '100%')
digit_considered_box.place(relx = 0.72, rely = 0.305)
digit_considered_box.insert(tk.END, '07')
response_box.place(relx = 0.72, rely = 0.405)
response_box.insert(tk.END, '07')
num_entry.place(anchor = 'se', relx = 0.35, rely = 0.694)


#---LEARNING---
working = app.frames['Learning']

#Buttons
update_rate_l = tk.Button(
    working, text = 'Set learning rate', width = 13,
    font = mainfont
    )
reset_l = tk.Button(working, text = 'Reset', width = 7, font = mainfont)
start_l = tk.Button(working, text = 'Start', width = 7, font = mainfont)
stop_l = tk.Button(working, text = 'Stop', width = 7, font = mainfont)
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
start_l.place(anchor = 'c', relx = 0.23, rely = 0.4)
stop_l.place(anchor = 'c', relx = 0.23, rely = 0.5)
goquery_l.place(anchor = 'c', relx = 0.23, rely = 0.9)
gohome_l.place(anchor = 'c', relx = 0.5, rely = 0.9)
exit_l.place(anchor = 'c', relx = 0.77, rely = 0.9)

# Labels and entries
learning_info_l = tk.Text(
    working, height = 5, width = 12, font = mainfont, insertontime = 0
)
speed_box_l = tk.Text(
    working, height = 1, width = 5, font = mainfont, insertontime = 0
)
speed_text_l = tk.Label(
    working, text = '• Current learning rate:', font = mainfont
)
error_text_l = tk.Label(
    working, text = '• Cost function value:', font = mainfont
)
error_box_l = tk.Text(
    working, height = 1, width = 5, font = mainfont, insertontime = 0
)
mode_text_l = tk.Label(
    working, text = "The Network's in training mode",
    font = mainfont
)
learning_rate_box_l = tk.Entry(working, font = mainfont, width = 5)

learning_rate_box_l.place(anchor = 'se', relx = 0.33, rely = 0.79)
learning_info_l.place(anchor = 'c', relx = 0.65, rely = 0.5)
error_box_l.place(relx = 0.725, rely = 0.2)
error_text_l.place(relx = 0.02, rely = 0.2)
speed_box_l.place(relx = 0.72, rely = 0.1)
speed_text_l.place(relx = 0.02, rely = 0.1)
mode_text_l.place(relx = 0.02, rely = 0.005)
speed_box_l.insert(tk.END, ' 0.3 ')
error_box_l.insert(tk.END, ' 12.3 ')
learning_info_l.insert(tk.END, 'Some info...')

app.mainloop()
