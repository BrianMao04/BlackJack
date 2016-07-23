#########################################
# Programmer: Brian Mao
# Date: 02/05/2014
# File Name: blackjack_classes0.py
# Description: Basic classes for making Blackjack game 
#########################################
import pygame, random
#----------------------------------#
class Card(object):
    """A standard playing card from a deck of 52 cards"""
    suit_names  =  ['club', 'diamond', 'heart', 'spade']
    rank_names  =  ['2','3','4','5','6','7','8','9','10','A','J','Q','K']
    
    def __init__(self,  suit=0,  rank=0):     #Card attributes
        self.suit  =  suit
        self.rank  =  rank
        self.value=0
        self.visible=True
        self.image = None
        self.image_back = pygame.image.load('cards_pictures\\back.png')
        self.update()
           
    def draw(self, surface, x=0, y=0):       #Give card ability to draw itself on the screen
        if self.visible==True:
            surface.blit(self.image,(x,y))   #Draw the front side of the card
        else:
            surface.blit(self.image_back,(x,y)) #Draw the back side of the card if it isn't flipped over

    def __str__(self):
        return self.suit_names[self.suit] + ' ' + self.rank_names[self.rank]

    def update(self):
        filepath = 'cards_pictures\\' + self.suit_names[self.suit] + '_' +  self.rank_names[self.rank] + '.png'
                                             #Assemble image paths based on properties of the card
        self.image = pygame.image.load(filepath)

        if self.rank<=8:                     #Value of cards of the first 8 elements in the list (ones that are not face cards or an ace)
            self.value=self.rank+2           #Accounting for list of cards starting at 2 and not 0 like the index
        elif self.rank>9 and self.rank<=12:  #Make all the face cards have a value of 10
            self.value=10
        else:
            self.value=11                    #Default value of an ace
            
    def show(self):                          #Flip card to face up
        self.visible = True

    def hide(self):                          #Flip card to face down
        self.visible = False
        
#---------------------------------------#
class Deck(object):
    """A standard deck of 52 Cards"""
    def __init__(self):
        self.cards = []
        self.gather()
        
    def __str__(self):                       #Converts deck to string for printing
        card_names = []
        for card in self.cards:
            card_names.append(str(card))
        return '\n'.join(card_names)
        
    def gather(self):
        for suit in range(4):                #Populates the deck with 4 suits,
            for rank in range(13):           #and 13 cards for each corresponding suit
                card = Card(suit,rank)
                card.update()
                self.cards.append(card)
                
    def checkempty(self):                    #Returns result of whether the deck has run out of cards
        return len(self.cards)==0
                

    def pop_card(self):                      #Removes and returns card from list of cards
        return self.cards.pop()
    
    def add_card(self, card):                #Adds card to list of cards
        self.cards.append(card)
        
    def shuffle(self):                       #Rearange order of cards in the deck
        random.shuffle(self.cards)
        
    def sort(self):                          #Sorts deck by suit
        self.cards.sort()
        
    def clear(self):                         #Empty the list of cards used when deal function is called to reset hands
        self.cards=[]
        
#---------------------------------------#
class Hand(Deck):  
    """A hand of cards, derived from Deck"""
    def __init__(self):                     #Create a list of cards
        self.cards=[]                       
        
    def calculatevalue(self):               #Calculate sum of cards in hand
        value=0
        acecount=0                           #Number of aces
        for i in range(len(self.cards)):
            value=value+ self.cards[i].value #Index of card with value associated with it
            if self.cards[i].rank==9:        #Check if the card is an ace
                acecount=acecount+1   
        while value>21 and acecount>0:       #Check if there is an ace in the hand and if the a bust would occur if the ace had a value of 11
            acecount=acecount-1
            value=value-10                   #Makes the ace a value of 1 instead of 11 by changing the value of the entire hand
            
        return value
        
    
    def drawhand(self, surface, x1=0, y1=0, spacing=10):
        if self.cards==[]:                  #Checks if it is not a blank list
            return                   
        
        #Gather information about the cards
        card_w = pygame.Surface.get_width(self.cards[0].image)
        card_h = pygame.Surface.get_height(self.cards[0].image)
        
        for i in range(len(self.cards)):    #Drawing cards in hand loop
            x = spacing+ x1 + i * (spacing + card_w)  #X-Coordiantes of the card based on an inital postion + spacing based off the numebr of cards in the hand
            y = y1                          #Y-Coorindates of the card that doesn't change
            self.cards[i].draw(surface, x, y)
            
#---------------------------
class Button(object):
    """ Pygame-based button """
    def __init__(self, text, x, y, w=100, h=40, hovercolour=(200,100,0), defcolour=(0,0,0)):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.hovercolour = hovercolour     #Colour of the button if mouse hovers over it
        self.defcolour = defcolour         #Default colour of the button when mouse is not hovering over it
        self.pressed = False                              
        self.hovering = False              #Mouse location
        self.font = pygame.font.Font('freesansbold.ttf', 32)    # Font object
        self.font_surf = None
        self.font_rect = None               #?
        self.setuptext()                   #Function Call

    def setuptext(self):
        # Sets up font surface
        self.font_surf=self.font.render(self.text, True, self.hovercolour)
        self.font_rect=self.font_surf.get_rect()
        self.font_rect.centerx=(self.rect.left + self.rect.right) / 2
        self.font_rect.centery=(self.rect.top + self.rect.bottom) / 2

    def update(self, events):
        # Get mouse position
        mousex=pygame.mouse.get_pos()[0]
        mousey=pygame.mouse.get_pos()[1]
        left=self.rect.left
        right=self.rect.right
        top=self.rect.bottom
        bottom=self.rect.top
        self.pressed = False
        
        if mousex>=left and mousex<=right and mousey>=bottom and mousey<=top:
            self.hovering=True
        else:
            self.hovering=False
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.hovering==True:
                self.pressed = True

    def draw(self, surface):
        # draw a button as a rectangle with text
        if self.hovering==True:
            pygame.draw.rect(surface, self.hovercolour, self.rect, 5)
            self.font_surf = self.font.render(self.text, True, self.hovercolour) #output 1 situation
        else:
            pygame.draw.rect(surface, self.defcolour, self.rect, 5)
            self.font_surf = self.font.render(self.text, True, self.defcolour) #output another situaiton default colour
        surface.blit(self.font_surf, self.font_rect) #copy onto game window
 

