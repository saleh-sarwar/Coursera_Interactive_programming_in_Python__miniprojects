#"Stopwatch: The Game"

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# define global variables
time = 0
stop = 0
bullseye = 0

# helper function format that converts time into formatted string A:BC.D
def format(time):
    D = time % 10
    C = (time // 10) % 10
    B = (time // 100) % 6
    A = time // 600
    return f"{A}:{B}{C}.{D}"

# define event handlers for buttons; "Start", "Stop", "Reset"
def timer_start():
    global running 
    timer.start()
    running = True

def timer_stop():    
    global stop, bullseye, running
    if running:
        timer.stop()
        stop += 1
        running = False
        if time % 10 == 0:
            bullseye += 1

def timer_reset():
    timer.stop()
    global time, stop, bullseye
    time = 0
    stop = 0
    bullseye = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1

# define draw handler
def draw_handler(canvas):
    global stop, bullseye
    canvas.draw_text(format(time), (80, 100), 24, 'White')
    canvas.draw_text(str(stop), (180, 20), 20, "Red")
    canvas.draw_text("/", (175, 20), 20, "Red")
    canvas.draw_text(str(bullseye), (165, 20), 20, "Red")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 200,200)
timer = simplegui.create_timer(100, tick)
frame.set_draw_handler(draw_handler)
frame.add_button("Start", timer_start, 100)
frame.add_button("Stop", timer_stop, 100)
frame.add_button("Reset", timer_reset, 100)

# start frame
frame.start()