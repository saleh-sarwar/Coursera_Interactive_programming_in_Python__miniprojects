#card game - Memory

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

turn = 0
# helper function to initialize globals
def new_game():
    global cards, exposed, state, turn
    cards = list(range(8)) + list(range(8))
    random.shuffle(cards)
    exposed = [ False ] * 16
    state = 0 
    turn = 0
    label.set_text(f"Turns: {turn}")
    
# define event handlers
def mouseclick(pos):
    global state, first_card, second_card, first_card_index, second_card_index,exposed
    global cards, turn
    # add game state logic here
    card_index = pos[0] // 50
    if not exposed[card_index]:
        if state == 0:
            first_card_index = card_index
            exposed[first_card_index] = True
            first_card = cards[first_card_index]
            state = 1
        elif state == 1:
            second_card_index = card_index
            if second_card_index != first_card_index:
                exposed[second_card_index] = True
                second_card = cards[second_card_index]
                state = 2
        elif state == 2:
            if first_card != second_card:
                exposed[first_card_index] = False
                exposed[second_card_index] = False
            first_card_index = card_index
            exposed[first_card_index] = True
            first_card = cards[first_card_index]
            state = 1
            turn += 1
        
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards
    width = 0
    for card_index in range(len(cards)):
        card_pos = 50 * card_index
        if exposed[card_index]:
            canvas.draw_text(str(cards[card_index]), [card_pos, 75], 75, "White")
        else:
            canvas.draw_polygon([(0 + width, 0), (50 + width, 0), (50 + width, 100), (0 + width, 100)],
                                1, 'Blue', 'White')
        width += 50
    label.set_text(f"Turns: {turn}")
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns: 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

