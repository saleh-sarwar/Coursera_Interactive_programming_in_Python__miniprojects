# Implementation of classic arcade game "Pong"

import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [ 0, 0]
ball_vel = [0, 0]
MOVE_INC = 12
SPEED = 1.1
hoshyari = " "

# initialize ball_pos and ball_vel for new bal in middle of table

def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [ WIDTH / 2, HEIGHT / 2]
    horizental_vel = random.randrange(4, 6)
    vertical_vel = random.randrange(3, 6)
    if direction == RIGHT:
        ball_vel = [horizental_vel, -1 * vertical_vel]
    else:
        ball_vel = [-1 * horizental_vel, -1 * vertical_vel]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos 
    global ball_vel,paddle1_vel, paddle2_vel, hoshyari
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
   
    
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #ball collide and refelect off the top and bottom as well as paddle
    collision()
    # Determines what happens when ball touches the gutter
    gutter()
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if HEIGHT - HALF_PAD_HEIGHT >= paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if HEIGHT - HALF_PAD_HEIGHT >= paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], 
                     [HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], 
                     [WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 
                     PAD_WIDTH, "White")
    
    # draw scores
    canvas.draw_text(str(score1), [ (WIDTH / 2) - 50, 30], 25, "White")
    canvas.draw_text(str(score2), [ (WIDTH / 2) + 50, 30], 25, "White")
    canvas.draw_text(hoshyari, [(WIDTH /2 ) - 150, HEIGHT / 2], 40, "White")

def gutter():
    global score1, score2
    if ball_pos[0] <= PAD_WIDTH:
        spawn_ball(RIGHT)
        score2 += 1
    elif ball_pos[0] >= WIDTH - PAD_WIDTH:
        spawn_ball(LEFT)
        score1 += 1

def collision():
    #ball collide and refelect off the top and bottom
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # determine whether paddle and ball collide    
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos + HALF_PAD_HEIGHT > ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0] * SPEED
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        if paddle2_pos + HALF_PAD_HEIGHT > ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] = ball_vel[0] * SPEED

def keydown(key):
    global paddle1_vel, paddle2_vel, hoshyari
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= MOVE_INC
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += MOVE_INC
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= MOVE_INC
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += MOVE_INC
                                   
   
def keyup(key):
    global paddle1_vel, paddle2_vel, hoshyari
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += MOVE_INC
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel -= MOVE_INC
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel += MOVE_INC
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel -= MOVE_INC
    
        
def restart():
    new_game()
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 100)

# start frame
new_game()
frame.start()
