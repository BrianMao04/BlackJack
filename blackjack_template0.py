#########################################
# Programmer: Brian Mao
# Date: 21/11/2012
# File Name: blackjack_template0.py
# Description: 
#########################################
#deal funcitons makes 3-5 cards (maybe not anymore)

#1.*ERASE PREVIOUS WIN MESSAGES!!!!!!!!!!!!!!! (I think it wokrs, but the last prblem of bool conditioons is sitll not fixed)
#2.deck runs out of cards and crashes game only when hit is pressed as well

#4.score coutns for ticks (most of the time)
#3.*no other button wokrs after hitting deal a second time

#5.make ace work for 1/11

#polish code +commenting


#pilotwings resort*
# wii sports
#checker knights
#mario 2
#star wolf theme
#startropics*
#baten kaitos*

#Could Try:
#populate funciton in deck class (still fails)
#msg outputting isntead


from blackjack_classes0 import *
import pygame
pygame.init()

WIDTH = 640
HEIGHT = 480
surface = pygame.display.set_mode((WIDTH, HEIGHT))

#---------------------------------------#
#   Colours                             #
#---------------------------------------#
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 200, 0

#-----------------
#Text Fonts
#-----------------
genericfont1=pygame.font.Font('freesansbold.ttf', 20)
genericfont2=pygame.font.Font('freesansbold.ttf', 35)  
#genericfont3=pygame.font.Font('freesansbold.ttf', 110)
#creditsfont=pygame.font.Font('freesansbold.ttf', 20)

#---------------------------------------#
#   Functions                           #
#---------------------------------------#
def deal(deck, player, dealer):  #fails when deck runs out of cards
    global reset , playerwin, dealerwin, message #doesn;t work for some reason ; **only wokrs veyr first game for soem reason
    playerwin=False
    dealerwin=False
    reset=True  #??
    
    if deck.checkempty()==True:  #reset deck when out of cards
        deck.gather()
    
    dealer.clear()
    player.clear()
    
    deck.shuffle()
    #message='lalallala'
    
    pick = deck.pop_card()   #take card form deck
    player.add_card(pick)   #add that card to the player
    pick = deck.pop_card()  #chosses and adds card to dealer's hand
    dealer.add_card(pick)   #ad that card to the dealer
    
    pick = deck.pop_card() #do all that a second itme
    player.add_card(pick)
    pick = deck.pop_card()
    dealer.add_card(pick)

    dealer.cards[1].hide()


def hit(deck):
    if deck.checkempty():
        deck.gather()
    player.add_card(deck.pop_card())
    
def dealerhit():
    if dealer.calculatevalue()<17:
        dealer.add_card(deck.pop_card())
        
def checkbust(hand):
    return hand.calculatevalue()>21
            

#Text Drawing Function
def text(text,cord,genericfont2,clr=WHITE):     
    text=str(text)
    fontsurface= genericfont2.render(text, False, clr)            #Render the text onto the new surface
    fontrect=fontsurface.get_rect()                               #Get boundaries of text surface
    fontrect.center=cord                                          #Center of text surface becomes cord parameter
    surface.blit(fontsurface,fontrect)                        #Copy font surface into game window

def redraw_game_window(surface,buttons, message):
    surface.fill(GREEN)
    player.drawhand(surface, y1=HEIGHT/2+100)               # draw player hand lower
    dealer.drawhand(surface,y1=120)  #draw dealer's ahnd 

    text('Dealer',(100, 100), genericfont1)                # draw "dealer" text
    text('Player', (100, HEIGHT / 2 + 70), genericfont1)  # draw "player" text
    text('Score: '+ str(score), (80,40), genericfont2, BLACK ) # draw score
    text(message, (480, 80), genericfont1)                    # draw message

    for button in buttons:                              # draw buttons
        button.draw(surface)
        
##    if checkbust(player)==True and reset==False:
##        text('Bust!',(400, HEIGHT/2 + 90), genericfont1)
##    if checkbust(dealer)==True and reset==False:
##        text('The dealer busted!!',(400, 100), genericfont1)
##
##    if playerwin==True and reset==False:
##        text('You Win!',(400, HEIGHT/2 + 70), genericfont1)
##    if dealerwin==True and reset==False:
##        text('Dealer Wins.',(400, HEIGHT/2 + 50), genericfont1)
    
    pygame.display.update()     
    
#---------------------------------------#
#   Main Program                        #
#---------------------------------------#
deck = Deck()
deck.shuffle()

player = Hand()
dealer = Hand()

deal(deck, player, dealer)

btn_deal = Button('Deal', 220, 20) 
btn_hit = Button('Hit', 350, 20)
btn_stand = Button('Stand', 480, 20)

score=0
gameon=True

playersturn=True
dealersturn=False   #----works

playerwin=False
dealerwin=False

scorechange=False
reset=False #is the game restartigng right here check
message = ''
#Play Music
#pygame.mixer.music.load("raymanl.mp3")                       #Soundtrack used
#pygame.mixer.music.play(-1)                                  #Makes soundtrack play throughout the whole game


while gameon==True:  #use later
    keys = pygame.key.get_pressed()
    events = pygame.event.get()
   
    
    if keys [pygame.K_ESCAPE]:
        gameon=False  #exit game if ESC key is pressed

    btn_deal.update(events)                         # update game buttons
    btn_hit.update(events)
    btn_stand.update(events)
    
    #chekcs which buttons are pressed
    if btn_deal.pressed==True:   #deal button
        deal(deck, player, dealer)
        message = 'lalallala' #why does this skip?!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        playersturn=True
        dealersturn=False
#player's turn
    if btn_hit.pressed==True and playersturn==True:
        hit(deck)                        #hit button  (right arguement?)
        
        if checkbust(player)==True:  #End if player busts
            playersturn=False
            dealerwin=True   #delaer wins if palyer busts
            dealersturn=False  #delaer doens;t even ened to paly if player busts
            message='Player went bust!'
            
            score=score-1
            reset=False
         
    if btn_stand.pressed==True and playersturn==True:    #stand button
        playersturn=False
        dealersturn=True
        
#Dealer's turn  *******bust fails (not anymore)
    if playersturn==False and dealersturn==True: 
        dealer.cards[1].show()
        if dealer.calculatevalue()<17:  #keep hitting unitl sum is over 16
            dealerhit()
            
        else:
            #dealer.calculatevalue()>=17:  #stop when 17 or above
            dealersturn=False
        
        if checkbust(dealer)==True:
            dealersturn=False  #only false after both palyers turn ends
            playerwin=True
            message = 'Dealer went bust!'
            
            score=score+1   #FIX!!!!!!!!!!!!! all scores
            scorechange=True
            reset=False
            
#check who wins
            
    if player.calculatevalue()> dealer.calculatevalue() and dealersturn==False and checkbust(player)==False:
        playerwin=True  #why is this satisying?
        message = 'Player wins!'
        
        score=score+1
        reset=False

    if dealer.calculatevalue()>= player.calculatevalue() and dealersturn==False and checkbust(dealer)==False:
        dealerwin=True
        message='Dealer wins'
        
        score=score-1
        reset=False
        
    redraw_game_window(surface, (btn_deal, btn_hit, btn_stand), message)
    
    
    #Check conditions---------------------------
    
    print 'Is it the dealers turn?',dealersturn 
    print 'playersturn?', playersturn
    
    print 'player wins in general ',playerwin   
    print 'dealers wins in general',dealerwin 
    
    print 'player bust? ',checkbust(player)
    print 'dealer bust? ',checkbust(dealer)
#   player.calculatevalue()> dealer.calculatevalue()
#    dealer.calculatevalue()>= player.calculatevalue()
    
    print 'Dealer wins by value: ',dealer.calculatevalue()>=player.calculatevalue()
    print 'player wins by value: ',player.calculatevalue()>dealer.calculatevalue()

    print 'reset?', reset  
            
    pygame.time.delay(20)
    
pygame.quit() #exit pygame when game is complete




#------------------------------------------
# Now, pop some cards from the deck and add them to the
# player's and dealer's hands, which are printed above.
#
# Try to sort the deck and print it. Why is it not sorted? Fix it!
#
# Use provided pictures and try to figure out how to draw a card
# on a "table" and how to draw a complete hand of cards.


##    print "Attributes of Card object:"
##    print "     Data:"
##    print "         self.suit"
##    print "         self.rank"
##    print "     Behaviour:"
##    print "         self.update()"
##    print ""
##    print "Attributes of Deck and Hand objects:"
##    print "     Data:"
##    print "         self.cards"
##    print "     Behaviour:"
##    print "         self.pop_card()"
##    print "         self.add_card()"
##    print "         self.shuffle()"
##    print "         self.sort()"
##    print "         self.update()\n"
##
##    print "Player's hand:\n",player, '\n'
##    print "Dealer's hand:\n",dealer, '\n'
##
##
##    print "value:"
##    print player.calculatevalue()

#--------------------------------
#probably cut out
##def titlescreen(): 
##    global gameon
##    while gameon:
##        game_window.fill(BLACK)
##        text("BlackJack", ((WIDTH/2),100),titlefont3,WHITE)
##        text("Python Edition", ((WIDTH/2),200),genericfont4,GREY)
##        text("Instructions", ((WIDTH/2),300),titlefont4,YELLOW)
##        text("Use the arrow keys to move.", ((WIDTH/2),360),titlefont2,BLUE)
##        text("Collect apples to score.", ((WIDTH/2),400),titlefont2,ORANGE)
##        text("Red: Increases score by 1 and lengthens snake", ((WIDTH/2),440),titlefont1,RED)
##        text("Poison Green: Decreases score by 1 (does NOT shorten snake)", ((WIDTH/2),470),titlefont1,GREEN)
##        text("Golden: Increases Score by 3 (does NOT lengthen snake)", ((WIDTH/2),500),titlefont1,YELLOW)
##        text("Hit space to play.", ((WIDTH/2),600),genericfont4)
##        text("Hit ESC to exit.", ((WIDTH/2),700),genericfont4)
##        pygame.event.get()
##        keys=pygame.key.get_pressed()
##        
##        if keys [pygame.K_SPACE]:                              #Proceed onto the game after the space bar is pressed
##            #timeron=True
##            break
##        pygame.display.update()
##        pygame.time.delay(1)
##
##        if keys[pygame.K_ESCAPE]:                              #Exit the game if the ESC key is pressed
##            gameon = False
##            #closegame()
##            
###Function used to control the outputs onto the game over screen
##def gameoverscreen():
##        game_window.fill(BLACK)
##        text("Final Score: ", ((WIDTH/2-160),50),genericfont2,GREEN)  
##        text(score,(WIDTH/2+50,50),genericfont1)
##        text("Time: ", ((WIDTH/2-130),110),genericfont2,GREEN)
##        text(int(timer), ((WIDTH/2+20),110),genericfont2,GREEN)
##        text("Game Over",((WIDTH/2),300),genericfont3,WHITE)
##        pygame.display.update()
##        pygame.time.delay(3000)                               #Delay for 3 seconds to percieve the screen
##        
##        #Display Credits
##        game_window.fill(BLACK)
##        text("Credits", ((WIDTH/2),70),genericfont3,YELLOW)
##        text("Template by: Mr.Grigorov", ((WIDTH/2),200),genericfont2,GREY)
##        text("Modified by: Brian Mao", ((WIDTH/2),150),genericfont2,WHITE)
##        text("Special Thanks to: Kenneth Sinder & Sam Raisbeck", ((WIDTH/2),270),creditsfont,BLUE)
##        text("Soundtrack: Rayman Legends: Grannies World Tour", (WIDTH/2,300),creditsfont,PURPLE)
##                 
##        game_window.blit(picture, ((WIDTH/2-100),350))
##        pygame.display.update()
##        pygame.time.delay(4000)                               #Delay for 4 seconds to percieve the screen
##

