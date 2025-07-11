# Please setup the distance on the tester to 9.5cm (ruler on the side)

import RPi.GPIO as GPIO
import sys
from tkinter import *
import tkinter.font as tkFont
import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep
from hx711 import HX711

GPIO.setwarnings(False)

# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

############################################################################################
# Direction pin from controller
DIR = 10
# Step pin from controller
STEP = 8
# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)


###########################################################################################   
hx = HX711(6,5)
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

def Loadcell():
    val = hx.get_weight(5)

    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
        
    return
    
############################################################################################
#Proximeter

#set GPIO Pins
T = 16
E = 26

#set GPIO direction (IN/OUT)
GPIO.setup(T, GPIO.OUT)
GPIO.setup(E, GPIO.IN)
GPIO.setwarnings(False)

def distance():
    #set Trigger to HIGH
    GPIO.output(T, True)
    
    #set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(T, False)

    StartTime = time.time()
    StopTime = time.time()

    #save StartTime
    while GPIO.input(E) == 0:
        StartTime = time.time()

    #save time of arrival
    while GPIO.input(E) == 1:
        StopTime = time.time()

    #time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    #multiply with the sonic speed (34300 cm/s
    #and divide by 2
    distance = (TimeElapsed * 34300)/2

    return distance
    
############################################################################################
def forward():
    dir = 1
    run_simple(dir)
    return

def backward():
    dir = 0
    run_simple(dir)
    return

def f_start():
    dir = 1
    run(dir)
    return

def b_start():
    dir = 0
    run(dir)
    return

def run_simple(dir):
    sleep(1.0)

    if dir == 1:
        GPIO.output(DIR,1)
        # Run for 7.5mm. For 200 steps = 1 rotation, 12 rotations = 1mm on the machine. This will change based on how you set you controller
        for x in range(18000):
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            sleep(.0005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.0005) # Dictates how fast stepper motor will run
    
    if dir == 0:
        GPIO.output(DIR,0)
        # Run for 7.5mm. For 200 steps = 1 rotation, 12 rotations = 1mm on the machine. This will change based on how you set you controller
        for x in range(18000):
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            sleep(.0005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.0005) # Dictates how fast stepper motor will run
    return

def run(dir):
    sleep(1.0)

    if dir == 1:
        GPIO.output(DIR,1)
        # Run for 35mm. For 200 steps = 1 rotation, 12 rotations = 1mm on the machine. This will change based on how you set you controller
        for x in range(84000):
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            sleep(.0005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.0005) # Dictates how fast stepper motor will run
    
    if dir == 0:
        GPIO.output(DIR,0)
        # Run for 35mm. For 200 steps = 1 rotation, 12 rotations = 1mm on the machine. This will change based on how you set you controller
        for x in range(84000):
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            sleep(.0005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.0005) # Dictates how fast stepper motor will run
    return

############################################################################################
# Parameters of screen and animations
update_interval = 60000 # Time (ms) between polling/animation updates
max_elements = 1440     # Maximum number of elements to store in plot lists

# Declare global variables
root = None
dfont = None
frame = None
canvas = None
ax1 = None
stress_strain = None

# Global variable to remember various states
fullscreen = False
stress_strain_visible = True

# Toggle fullscreen
def toggle_fullscreen(event=None):

    global root
    global fullscreen

    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)

# Return to windowed mode
def end_fullscreen(event=None):

    global root
    global fullscreen

    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)

# Automatically resize font size based on window size
def resize(event=None):

    global dfont
    global frame

    # Resize font based on frame height (minimum size of 12)
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 15)))
    dfont.configure(size=new_size)
    
# Toggle the stress vs strain plot
def stressstrain():

    global canvas
    global ax1
    global stress_strain

    # Toggle plot and axis ticks/label
    stress_strain = not stress_strain
    ax1.collections[0].set_visible(stress_strain_visible)
    ax1.get_xaxis().set_visible(stress_strain_visible)
    ax1.get_yaxis().set_visible(stress_strain_visible)
    canvas.draw()

# This function is called periodically from FuncAnimation
def animate(i, ax1, s, e, Sigma, Epsilon):
    
    # Update data to display force and distance
    try:
        
        global sigma
        global epsilon
        
        sigma = Loadcell() * 35
        epsilon = 716.28313 * (35 - (distance()- 6.5))
        
    except NameError:
        return "NameEror ocurred. Some variable isn't defined"

    # Update our labels
    Sigma.set(sigma)
    Epsilon.set(epsilon)

    # Append sensor data to lists for plotting
    s.append(sigma)
    e.append(epsilon)

    # Limit lists to a set number of elements
    s = s[-max_elements:]
    e = e[-max_elements:]

    # Clear, format, and plot 
    color = 'tab:blue'
    ax1.clear()
    ax1.set_xlabel("Strain", color=color)
    ax1.set_ylabel('Stress', color=color)
    ax1.tick_params(axis='both', labelcolor=color)
    ax1.plot(s, e , linewidth=2, color=color)
    

    # Make sure plots stay visible or invisible as desired
    ax1.collections[0].set_visible(stress_strain_visible)

# Dummy function prevents segfault
def _destroy(event):
    pass


############################################################################################
# Start function to move the motor and return

def start():
    f_start()
    sleep(5.0)
    b_start()
    
############################################################################################
#Main script

# Create the main window
root = Tk()
root.title("Tensile Test Machine")

# Create the main container
frame = Frame(root)
frame.configure(bg='white')

# Lay out the main container (expand to fit window)
frame.pack(fill=BOTH, expand=1)

# Create figure for plotting
fig = figure.Figure(figsize=(2, 2))
fig.subplots_adjust(left=0.1, right=0.8)
ax1 = fig.add_subplot(1, 1, 1)

#Empty x and y lists to store data for plot
s = []
e = []

Sigma = DoubleVar()
Epsilon = DoubleVar()

# Create dynamic font for text
dfont = tkFont.Font(size=-24)

# Create a Tk Canvas widget out of our figure
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_plot = canvas.get_tk_widget()

# Create other supporting widgets
b = Button()
b.pack()
        
button_start = Button(    frame,
                            text="Start",
                            font=dfont,
                            command= start)
button_stop = Button(   frame,
                            text="Stop",
                            font=dfont,
                            command= root.destroy)
button_forward = Button(    frame,
                            text="Forward",
                            font=dfont,
                            command= forward)
button_backwards = Button(    frame,
                            text="Backwards",
                            font=dfont,
                            command= backward)
                    
# Lay out widgets in a grid in the frame
canvas_plot.grid(   row=0,
                    column=0,
                    rowspan=5,
                    columnspan=4,
                    )
button_start.grid(row=5, column=0, columnspan=2)
button_stop.grid(row=5, column=2, columnspan=2)
button_forward.grid(row=4, column=4, columnspan=2)
button_backwards.grid(row=5, column=4, columnspan=2)

# Add a standard 5 pixel padding to all widgets
for w in frame.winfo_children():
    w.grid(padx=5, pady=5)

# Make it so that the grid cells expand out to fill window
for i in range(0, 5):
    frame.rowconfigure(i, weight=1)
for i in range(0, 5):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)

# Call empty _destroy function on exit to prevent segmentation fault
root.bind("<Destroy>", _destroy)

# Call animate() function periodically
fargs = (ax1, s, e, Sigma, Epsilon)
ani = animation.FuncAnimation(  fig,
                                animate,
                                fargs=fargs,
                                interval=update_interval)

# Start in fullscreen mode and run
toggle_fullscreen()
root.mainloop()
