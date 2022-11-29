# Rock-paper-scissors-lizard-Spock


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# helper functions

def name_to_number(name):
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    

def number_to_name(number):
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print("incorrect option selected")
    

def rpsls(player_choice): 
    print("")
    
    # prints out the message for the player's choice
    print(f"Player chooses {player_choice}")
    
    # converts the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # computes random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)	
    
    # converts comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
 
    # computes difference of comp_number and player_number modulo five
    diff = ((player_number - comp_number) % 5) 
    
    # prints out the message for computer's choice
    print(f"Computer chooses {comp_choice}")
    
    # use if/elif/else to determine winner, print winner message
    if diff == 1 or diff == 2:
        print("Player wins!")
    elif diff == 3 or diff == 4:
        print("Computer wins!")
    else:
        print("Player and computer tie!")

# Handler for player input

def get_input(inp):
    if not ( inp == "rock" or inp == "paper" or inp == "scissors" or
            inp == "lizard" or inp == "Spock"):
        print("Error: You haven't entered a valid choice")
    else:
        rpsls(inp)
    

#Create frames and assign callbacks to event handler

frame = simplegui.create_frame("rock-paper-scissors-lizard-Spock", 200,200)
frame.add_input("Enter your choice:", get_input, 100)

#Start the frame animations

frame.start()





