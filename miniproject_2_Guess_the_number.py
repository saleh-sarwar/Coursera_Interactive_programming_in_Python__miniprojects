# Guess the number

# input will come from buttons and an input field
# all output for the game will be printed in the console


import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# initializing global variables
high_num_range = 100
secret_number = 0
num_guess = 0

# helper function to start and restart the game
def new_game():
    global secret_number, high_num_range, num_guess
    secret_number = random.randrange(0,high_num_range)
    
    # setting the value of number of guesses based on the range
    
    if high_num_range == 100:
        num_guess = 7
    else:
        num_guess = 10
    
    print(f"New game. Range is from 0 to {high_num_range}")
    print(f"Number of remaining guesses is {num_guess}")
    print("")
    
# define event handlers for control panel

def range100():
    global high_num_range
    high_num_range = 100
    new_game()

def range1000():
    global high_num_range
    high_num_range = 1000
    new_game()
    
def input_guess(guess):
    print(f"Guess was {guess}")
    global num_guess
    if num_guess == 1:
        print("Incorrect!")
        print("Game over! You used all of your tries")
        print("")
        new_game()
    elif int(guess) == secret_number:
        print("Correct!")
        print("")
        new_game()
    elif int(guess) > secret_number:
        num_guess -= 1
        print(f"Number of remaining guesses is {num_guess}")
        print("Higher!")
        print("")
    else:
        num_guess -= 1
        print(f"Number of remaining guesses is {num_guess}")
        print("Lower!")
        print("")
    
# create frame

frame = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements and start frame

frame.add_input("Enter your guess:", input_guess, 190)
frame.add_button("Range is (0, 100]", range100, 200)
frame.add_button("Range is (0, 1000]", range1000, 200)
frame.start()

# call new_game 
new_game()


