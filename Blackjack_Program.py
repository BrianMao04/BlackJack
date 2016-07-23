#########################################
# Template by: Mr. Grigorov
# Modified by: Brian Mao"
# Date: 03/05/2014
# File Name: blackjack_template0.py
# Description: This program is for a Blackjack game and imports classes in another module
#########################################

from Blackjack_Main_Classes01 import *
import pygame
pygame.init()

WIDTH = 640                                               #Game window dimensions
HEIGHT = 620
surface = pygame.display.set_mode((WIDTH, HEIGHT))

#---------------------------------------#
#   Colours                             #
#---------------------------------------#
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 200, 0
RED   = 255, 0, 50
GREY  = 50, 50, 50  

#-----------------
#Text Fonts
#-----------------
titlefont=pygame.font.Font('freesansbold.ttf', 50)
genericfont1=pygame.font.Font('freesansbold.ttf', 30)
genericfont2=pygame.font.Font('freesansbold.ttf', 35)
genericfont3=pygame.font.Font('freesansbold.ttf', 15)
genericfont4=pygame.font.Font('freesansbold.ttf', 25)

#---------------------------------------#
#   Functions                           #
#---------------------------------------#
def hit(deck):
    if deck.checkempty():                                 #Repopulate the deck if it is empty
        deck.gather()    
    player.add_card(deck.pop_card())                      #Add a card to the player's hand
    
def dealerhit(deck):
    if deck.checkempty():                                 #Repopulate the deck if it is empty
        deck.gather()
    if dealer.calculatevalue()<17:                        #Add a card to the dealer's hand if it's value is below 17
        dealer.add_card(deck.pop_card())
        
def deal(deck, player, dealer):  
    if deck.checkempty()==True:                           #Repopulate the deck if it is empty
        deck.gather()  
    
    dealer.clear()                                        #Remove all of the dealer's cards
    player.clear()                                        #Remove all of the player's cards
    
    deck.shuffle()                                        #Rearange the order of all the cards
    
    for i in range(2):                                    #Populate hands with 2 cards each
        hit(deck)
        dealerhit(deck)
    
    dealer.cards[1].hide()                                #Ouput the back of the dealer's second card instead of the front

def checkbust(hand):
    return hand.calculatevalue()>21
            

#Text Drawing Function
def text(text,cord,genericfont2,clr=WHITE):     
    text=str(text)
    fontsurface= genericfont2.render(text, False, clr)   #Render the text onto the new surface
    fontrect=fontsurface.get_rect()                      #Get boundaries of text surface
    fontrect.center=cord                                 #Center of text surface becomes cord parameter
    surface.blit(fontsurface,fontrect)                   #Copy font surface into game window

def redraw_game_window(surface,buttons, message):
    surface.fill(GREEN)                                  #Background Colour
    player.drawhand(surface, y1=340)                     #Draw player's hand
    dealer.drawhand(surface,y1=120)                      #Draw dealer's hand
    
    text('BlackJack',(WIDTH/2,40), titlefont, GREY)
    text('Dealer',(100, 100), genericfont1)             #Draw "Dealer" text
    text('Player', (100, 320), genericfont1)            #Draw "Player" text
    text('Score: '+ str(score), (WIDTH/2+220,100), genericfont2, RED )   # Draw "Score" and it's value
    text('Hit ESC to Close Game',(540, 600), genericfont3) 
    text(message, (420, 280), genericfont4, RED)        # Draw a message absed off game outcome

    for button in buttons:                              #Draw buttons
        button.draw(surface)
    
    pygame.display.update()     
    
#---------------------------------------#
#   Main Program                        #
#---------------------------------------#
deck = Deck()
deck.shuffle()

player = Hand()
dealer = Hand()

btn_deal = Button('Deal', 130, 530) 
btn_hit = Button('Hit', 260, 530)
btn_stand = Button('Stand', 390, 530)

gameon=True  

playersturn=True                                     #Default values when game first starts
dealersturn=False   

playerwin=False
dealerwin=False
roundend=False                                       #Detects if the round should end

score = 0
message = ''                                         #Message to be outputted onto the game window

deal(deck, player, dealer)                           #Begin game with deal function already called upon once

#Play Music
pygame.mixer.music.load("pokemonpt.mp3")             #Soundtrack used
pygame.mixer.music.play(-1)                          #Makes soundtrack play throughout the whole game


while gameon==True: 
    keys = pygame.key.get_pressed()                  #Detect player actions in game
    events = pygame.event.get()
    
    if keys [pygame.K_ESCAPE]:
        gameon=False                                 #Exit game if ESC key is pressed

    btn_deal.update(events)                          #Update game buttons
    btn_hit.update(events)
    btn_stand.update(events)
    
    #Checks if buttons are pressed
    if btn_deal.pressed==True:                     #Deal button
        deal(deck, player, dealer)
        message = ' '                              #Clear any previous message from previous game outcome
        playersturn=True                           #Activate player's turn when new game starts
        dealersturn=False                          #End the dealer's turn when a new game starts
        roundend=False
        
        playerwin=False                            #Neither the player or dealer is the winner at the start of a round
        dealerwin=False

#Player's Turn
    if btn_hit.pressed==True and playersturn==True:
        hit(deck)                                 #Hit button  
        
        if checkbust(player)==True:               #Check if player busts
            playersturn=False                     #End the player's turn
            dealerwin=True                        #Dealer wins if player busts
            dealersturn=False                     #Dealer doesn't even need to play if player busts
            
            dealer.cards[1].show()                #Flip over the dealer's second card
            message='Bust!   Dealer wins'
            score=score-1                         #Update the score
         
    if btn_stand.pressed==True and playersturn==True: #Stand button
        playersturn=False                         #End the player's turn
        dealersturn=True                          #Dealer's turn starts after the player's turn ends
        
#Dealer's Turn  
    if playersturn==False and dealersturn==True: 
        dealer.cards[1].show()                    #Flip over dealer's second card
        
        if checkbust(dealer)==True:               #Check if the dealer busts
            dealersturn=False                     #End the dealer's turn
            playerwin=True                        #Player wins if the dealer busts
            
            message = 'Dealer busts!   Player wins!'
            score=score+1                         #Update the score
            
        if dealer.calculatevalue()<17:            #Dealer keeps hitting unitl the sum of the hand is greater than 16
            dealerhit(deck)
            
        else:
            dealersturn=False                     #Dealer's turn ends after the sum of the hand is greater than 16
            roundend=True                         #Round ends if the sum of the hand of the dealer is greater than 16
            
#Check Who Wins          
    if player.calculatevalue()> dealer.calculatevalue() and dealersturn==False and checkbust(player)==False and roundend==True:
        playerwin=True                           #Player wins if their hand is greater than the dealer's, and they have not busted
        roundend=False                           #Restores default value of roundend for next round so the following if statement is not satisfied from the start

        message = 'Player Wins!'
        score=score+1                            #Update the score

    if dealer.calculatevalue()>= player.calculatevalue() and dealersturn==False and checkbust(dealer)==False and roundend==True:
        dealerwin=True                           #Dealer wins if their hand is greater than the player's, and they have not busted
        roundend=False                           #Restores default value of roundend for next round so the following if statement is not satisfied from the start

        message='Dealer Wins'
        score=score-1                           #Update the score
        
    redraw_game_window(surface, (btn_deal, btn_hit, btn_stand), message)  #Update the game window
            
    pygame.time.delay(10)
    
pygame.quit()                                 #Exit pygame when game is complete

print "Thanks for playing!"

if score>7:                                   #Highest score ever achieved while developing game
    print " "
    print "Congratulations! You beat the staff record!"
    
print " "
print "      Credits"
print "Template by: Mr. Grigorov"
print "Modified by: Brian Mao"
print "Soundtrack: Pokemon Colosseum Pyrite Town"
print "Special Thanks: Kenneth Sinder and Sam Raisbeck"
