#########################################
# Programmer: Kenneth Sinder (template by Mr. G)
# Date: April 25, 2014
# File Name: blackjack_main.py
# Description: The launching point of a Blackjack game
#########################################
import pygame
from blackjack_classes import *
from pygame.locals import *
pygame.init()

#---------------------------------------#
#   colours and fonts                   #
#---------------------------------------#
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREY = 100, 100, 100
font = pygame.font.Font('freesansbold.ttf', 20)

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def hit(hand, deck):
    if deck.is_empty():
        deck.populate()
    hand.add_card(deck.pop_card())

def deal(deck, player, dealer):
    player.clear()
    dealer.clear()
    deck = Deck()
    deck.shuffle()
    for i in range(2):
        player.add_card(deck.pop_card())
        dealer.add_card(deck.pop_card())
    dealer.cards[0].hide()

def draw_text(surface, text, x, y, colour=BLACK):
    font_surf = font.render(str(text), True, colour)
    font_rect = font_surf.get_rect()
    font_rect.center = (x, y)
    surface.blit(font_surf, font_rect)

def redraw_surface(surface, player, dealer, buttons, score, msg):
    surface.fill(WHITE)                                 # fill in the screen
    dealer.draw(surface, y1=140)                        # draw dealer hand
    player.draw(surface, y1=HEIGHT/2+100)               # draw player hand lower
    draw_text(surface, 'Dealer\'s Hand', 100, 100)      # draw text for both hands
    draw_text(surface, 'Player\'s Hand', 100, HEIGHT / 2 + 70) 
    draw_text(surface, 'Score: ' + str(score), 470, 40) # draw score
    draw_text(surface, msg, 480, 80)                    # draw message
    for button in buttons:                              # draw buttons
        button.draw(surface)
    pygame.display.flip()                               # update the display
    
#---------------------------------------#
#   main program                        #
#---------------------------------------#
WIDTH, HEIGHT = 1100, 480
display_surf = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
pygame.display.set_caption('Blackjack - Kenneth Sinder')
fps_clock = pygame.time.Clock()
FPS = 60

deck = Deck()
player = Hand()
dealer = Hand()
deal(deck, player, dealer)

btn_deal = Button('Deal', 20, 20)
btn_hit = Button('Hit', 150, 20)
btn_stand = Button('Stand', 280, 20)

in_play = True
player_control = True
waiting = False             # flag for whether or not player is expected to deal
score = 0
message = ''

while in_play:
    # check for quit events
    events = pygame.event.get()
    for event in events:                
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            in_play = False
    btn_deal.update(events)                         # update game buttons
    btn_hit.update(events)
    btn_stand.update(events)
    
    if btn_deal.pressed and waiting:                # deal button starts a new game
        deal(deck, player, dealer)
        player_control = True                       # player regains control
        waiting = False                             # no longer waiting for a new game
        message = ''                                # clear user message
    elif btn_hit.pressed and player_control and not waiting:      
        hit(player, deck)                           # hit button gives the player a new card
        if player.value() > 21:
            message = 'Player went bust!'
            score -= 1
            waiting = True
            message = message + ' Deal again?'
    elif btn_stand.pressed and player_control and not waiting:  
        player_control = False                      # stand button passes action to the dealer

    if not player_control and not waiting:
        dealer.cards[0].show()                  # reveal dealer's first card
        while dealer.value() < 17:              # dealer draws cards until value >= 17    
            hit(dealer, deck)                   
        if dealer.value() > 21:                 # dealer goes bust if hand value exceeds 21
            message = 'Dealer went bust!'
            score += 1
        elif player.value() > dealer.value():   # player wins if their value is higher
            message = 'Player wins!'
            score += 1
        else:                                   # otherwise, the dealer wins
            message = 'Dealer wins!'            
            score -= 1
        dealer.cards[0].show()                  # reveal dealer's first card
        waiting = True
        message = message + ' Deal again?'
    
    redraw_surface(display_surf, player, dealer,    # redraw the game window
                   (btn_deal, btn_hit, btn_stand), score, message)
    fps_clock.tick(FPS)                             # enforce the desired framerate
pygame.quit()

