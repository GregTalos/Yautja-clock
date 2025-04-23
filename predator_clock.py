import tkinter as tk
import math
import time
from datetime import datetime

# Constants
GRID_SIZE = 350
RADIUS = 80
DIGIT_COUNT = 6  # For HH:MM:SS

# 16 direction vectors
DIRECTIONS_16 = {
    0:  (0, -0.72),
    1:  (math.sqrt(2)/2, -math.sqrt(2)/2),
    2:  (0.72, 0),
    3:  (math.sqrt(2)/2, math.sqrt(2)/2),
    4:  (0, 0.72),
    5:  (-math.sqrt(2)/2, math.sqrt(2)/2),
    6:  (-0.72, 0),
    7:  (-math.sqrt(2)/2, -math.sqrt(2)/2),
    8:  (0, -0.72),
    9:  (math.sqrt(2)/2, -math.sqrt(2)/2),
    10: (0.72, 0),
    11: (math.sqrt(2)/2, math.sqrt(2)/2),
    12: (0, 0.72),
    13: (-math.sqrt(2)/2, math.sqrt(2)/2),
    14: (-0.72, 0),
    15: (-math.sqrt(2)/2, -math.sqrt(2)/2),
}

show_labels = True


def draw_segment(canvas, i, center_x, center_y, color, width):
    dx, dy = DIRECTIONS_16[i]
    offset_y = 0 if i < 8 else 110
    x1 = center_x
    y1 = center_y + offset_y
    x2 = center_x + dx * RADIUS
    y2 = center_y + dy * RADIUS + offset_y
    canvas.create_line(x1, y1, x2, y2, fill=color, width=width)


def draw_base_grid(canvas, center_x, center_y):
    for i in range(16):
        draw_segment(canvas, i, center_x, center_y, 'gray', 2)


def draw_yautja_segments(canvas, segments, center_x, center_y):
    for i, active in enumerate(segments):
        if active:
            draw_segment(canvas, i, center_x, center_y, 'red', 4)


def draw_digit(canvas, segments, digit_index, char=None, offset_x=100):
    spacing = 140
    center_x = offset_x + digit_index * spacing
    center_y = 80
    draw_base_grid(canvas, center_x, center_y)
    draw_yautja_segments(canvas, segments, center_x, center_y)
    if show_labels and char is not None:
        canvas.create_text(center_x, center_y + 180, text=char, fill='red', font=('DS-Digital', 24, 'bold'))


def animate_startup(canvas):
    spacing = 140
    center_y = 80
    steps = 30
    delay = 30
    total_digits = 10  # Show all 10 digits during startup

    canvas.config(width=100 + total_digits * spacing)

    for step in range(steps):
        canvas.delete("all")
        for digit_index in range(total_digits):
            center_x = 100 + digit_index * spacing
            draw_base_grid(canvas, center_x, center_y)
            angle_offset = int((step * (16 / steps)) % 16)
            active_segment = (angle_offset + digit_index * 2) % 16
            draw_segment(canvas, active_segment, center_x, center_y, 'red', 4)
        canvas.update()
        canvas.after(int(delay * (1.5 - abs(step - steps/2) / (steps/2))))

    canvas.delete("all")
    for digit_index in range(total_digits):
        center_x = 100 + digit_index * spacing
        for i in range(16):
            draw_segment(canvas, i, center_x, center_y, 'red', 4)
        canvas.create_text(center_x, center_y + 180, text=str(digit_index), fill='red', font=('DS-Digital', 24, 'bold'))
    canvas.update()
    canvas.after(3000)  # Hold for 3 seconds

    # Flash to black and reset
    for _ in range(2):
        canvas.delete("all")
        canvas.update()
        canvas.after(150)
        for digit_index in range(total_digits):
            center_x = 100 + digit_index * spacing
            draw_base_grid(canvas, center_x, center_y)
        canvas.update()
        canvas.after(150)

    # Animate canvas shrinking to clock width
    final_width = 100 + DIGIT_COUNT * spacing
    current_width = 100 + total_digits * spacing
    shrink_steps = 20
    for i in range(shrink_steps):
        interp_width = int(current_width - (current_width - final_width) * (i + 1) / shrink_steps)
        canvas.config(width=interp_width)
        canvas.update()
        canvas.after(50)

    global show_labels
    show_labels = False


# Yautja digit definitions (0–9)
digit_segments = [
    [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],  # 0
    [1,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0],  # 1
    [1,0,1,1,0,1,1,0,0,0,1,0,0,0,0,1],  # 2
    [0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,1],  # 3
    [0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,1],  # 4
    [1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,1],  # 5
    [0,0,0,1,0,1,0,0,0,1,1,0,1,0,0,1],  # 6
    [1,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0],  # 7
    [1,0,1,1,0,1,1,0,0,0,1,0,1,0,0,1],  # 8
    [1,0,1,1,0,1,1,0,0,1,1,0,1,0,0,1],  # 9
]

# --- TKINTER SETUP ---
root = tk.Tk()
root.title("Yautja Clock")
canvas_width = 100 + DIGIT_COUNT * 140
canvas = tk.Canvas(root, width=canvas_width, height=GRID_SIZE, bg='black')
canvas.pack()

# Run boot animation
animate_startup(canvas)

# --- LIVE CLOCK DISPLAY ---
def update_clock():
    canvas.delete("all")
    now = datetime.now().strftime("%H%M%S")
    for i, char in enumerate(now):
        segs = digit_segments[int(char)]
        draw_digit(canvas, segs, i, char)
    canvas.update()
    root.after(1000, update_clock)

# Toggle label visibility with spacebar
def on_key_press(event):
    global show_labels
    if event.keysym == 'space':
        show_labels = True

def on_key_release(event):
    global show_labels
    if event.keysym == 'space':
        show_labels = False

root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# Start clock loop
update_clock()
root.mainloop()