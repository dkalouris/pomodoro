from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #

# Color and font constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Countdown constants
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Checkmark constant for tracking number of work-sessions completed
CHECKMARK = "✔"

# Track current repetition index, to check if its work or break time
reps = 0

# Initialize object storing the current countdown
timer = None


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global reps, timer
    # Cancel any existing timer
    if timer is not None:
        window.after_cancel(timer)
    # Initialize timer text
    canvas.itemconfig(timer_text, text="00:00")
    top_text.config(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 35, "bold"))
    # Start timer
    start_timer(initial=True)


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer(initial=False):
    global timer
    # Cancel any existing timer
    if timer is not None:
        window.after_cancel(timer)
    global reps
    reps += 1
    # Check if this is the first time calling this function
    if initial:
        reps = 1
    # Convert minutes to seconds
    work_sec = WORK_MIN * 60
    short_break_secs = SHORT_BREAK_MIN * 60
    long_break_secs = LONG_BREAK_MIN * 60

    # Every other countdown is break countdown,
    # every 4th break is long break countdown, otherwise is a small break countdown
    # in any other case we got work countdown.
    if reps % 8 == 0:
        count_down(long_break_secs)
        top_text.config(text="Long break!!", fg=GREEN)
    elif reps % 2 == 0:
        count_down(short_break_secs)
        top_text.config(text="Small break!!", fg=GREEN)
    else:
        count_down(work_sec)
        top_text.config(text="Work time!", fg=RED)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 


def count_down(count):
    global reps
    num_min = math.floor(count / 60)
    num_sec = count % 60
    # Print countdown seconds in time format
    canvas.itemconfig(timer_text, text=f"{num_min:02d}:{num_sec:02d}")
    # Call next countdown
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    # If we finished counting down, calculate the number of work sessions (every other session)
    # and add checkmarks (see constant) accordingly
    elif count == 0:
        start_timer()
        work_sessions = math.floor(reps / 2)
        check_text.config(text=CHECKMARK * work_sessions)


# ---------------------------- UI SETUP ------------------------------- #

# Initialize window, with padding so that elements are shown better
window = Tk()
window.title("pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Create a canvas that we can add own objects
canvas = Canvas(width=350, height=224, bg=YELLOW, highlightthickness=0)

# Add the tomato image
my_tomato = PhotoImage(file="tomato.png")
canvas.create_image(175, 112, image=my_tomato)

# Add timer inside the tomato image
timer_text = canvas.create_text(175, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# Add text above tomato to show current countdown type
top_text = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
top_text.grid(row=0, column=1)

# Add button to start the countdown
button_start = Button(text="Start", highlightthickness=0, command=lambda: start_timer(initial=True))
button_start.grid(row=2, column=0)

# Add button to reset the countdown
button_reset = Button(text="Reset", highlightthickness=0, command=reset_timer)
button_reset.grid(row=2, column=2)

# Add foreground for adding the checkmarks later
check_text = Label(text="", fg=GREEN, bg=YELLOW)
check_text.grid(row=3, column=1)

window.mainloop()
