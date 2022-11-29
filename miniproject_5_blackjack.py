#  Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
message = ""
score = 0
outcome = ""
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print(f"Invalid card: {suit}, {rank}")

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ans = ""
        for card in self.cards:
            ans += str(card) + " "
        return f"Hand contains {ans}"

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        has_ace = False
        for card in self.cards:
            rank = card.get_rank()
            hand_value += VALUES[rank]
            if rank == "A":
                has_ace = True
        if has_ace == False:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            card.draw(canvas, [pos[0] + CARD_SIZE[0] * i, pos[1] ])
            i += 1
                
        
# define deck class 
class Deck:
    def __init__(self):
        deck = [ ]
        for i in SUITS:
            for j in RANKS:
                deck.append(Card(i, j))
        self.deck = deck

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        card = self.deck[-1]
        self.deck.pop()
        return card
    def __str__(self):
        ans = ""
        for card in self.deck:
            ans += str(card) + " "
        return f"Deck contains {ans}"

#define event handlers for buttons
def deal():
    global message, in_play, deck, player_hand, dealer_hand, outcome, score
    if in_play:
        score -= 1
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    in_play = True
    message = "Hit or stand?"
    outcome = ""

def hit():
    global message, outcome, in_play, score
    # if the hand is in play, hit the player
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You busted!"
            message = "New deal?"
            in_play = False
            score -= 1
      
def stand():
    global outcome, message, in_play, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    
    if dealer_hand.get_value() > 21:
        outcome = "Dealer busted!"
        score += 1
    elif player_hand.get_value() > dealer_hand.get_value():
        outcome = "Player won"
        score += 1
    else:
        outcome = "You busted!"
        score -= 1
    
    # assign a message to outcome, update in_play and score
    in_play = False
    message = "New deal?"

# draw handler    
def draw(canvas):
    global outcome, player_hand, dealer_hand, message, in_play, score
    
    # test to make sure that card.draw works, replace with your code below
    if in_play:
        dealer_hand.draw(canvas, [100, 200])
        canvas.draw_image(card_back , (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]),
                          CARD_BACK_SIZE, [100 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)    
    else:
        dealer_hand.draw(canvas, [100, 200])
    
    player_hand.draw(canvas, [100, 400])
    canvas.draw_text("Blackjack", [ 160, 50 ], 40, "White", "serif")
    canvas.draw_text(f"Dealer       {outcome}", [100, 160], 30, "Black")
    canvas.draw_text(f"Player       {message}", [100, 360], 30, "Black")
    canvas.draw_text(f"Score: {score}", [400, 50], 30, "Black") 

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
