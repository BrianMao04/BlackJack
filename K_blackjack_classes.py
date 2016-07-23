#########################################
# Programmer: Kenneth Sinder (template by Mr. G)
# Date: April 25, 2014
# File Name: blackjack_classes.py
# Description: Classes for a Blackjack game
#########################################
import pygame, random
from pygame.locals import *

class Card(object):
    """A standard playing card from a deck of 52 cards"""
    suit_names = ['club', 'diamond', 'heart', 'spade']
    rank_names = ['2','3','4','5','6','7','8','9','10','A','J','Q','K']
    
    def __init__(self, suit=0, rank=0):
        self.suit = suit
        self.rank = rank
        self.face_up = True
        self.image_back = pygame.image.load('cards_pictures\\back.png')
        self.image = None
        self.value = 0
        self.update()

    def __str__(self):
        return self.suit_names[self.suit] + ' ' + self.rank_names[self.rank]
 
    def update(self):
        image_path = 'cards_pictures\\' + self.suit_names[self.suit] + '_' + \
                  self.rank_names[self.rank] + '.png'
        self.image = pygame.image.load(image_path)
        if self.rank <= 8:
            self.value = self.rank + 2
        elif 10 <= self.rank <= 12:
            self.value = 10
        else:
            self.value = 11

    def draw(self, surface, x=0, y=0):
        if self.face_up:
            surface.blit(self.image, (x, y))
        else:
            surface.blit(self.image_back, (x, y))

    def show(self):
        self.face_up = True

    def hide(self):
        self.face_up = False
        
#---------------------------------------#
class Deck(object):
    """A standard deck of 52 Cards"""
    def __init__(self):
        self.cards = []
        self.populate()
                
    def __str__(self):
        card_names = []
        for card in self.cards:
            card_names.append(str(card))
        return '\n'.join(card_names)

    def update(self):
        pass

    def pop_card(self):
        return self.cards.pop()
    
    def add_card(self, card):
        self.cards.append(card)
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def sort(self):
        self.cards.sort(key = lambda x: (x.suit, x.rank))

    def clear(self):
        self.cards = []

    def is_empty(self):
        return len(self.cards) == 0

    def populate(self):
        for suit in range(4):
            for rank in range(13):
                card = Card(suit, rank)
                self.cards.append(card)
        
#---------------------------------------#
class Hand(Deck):
    """a hand of cards, derived from Deck"""
    def __init__(self):
        self.cards = []

    def update(self):
        pass
    
    def value(self):
        result = 0; aces = 0
        for card in self.cards:
            result += card.value
            if card.rank == 9:
                aces += 1
        while result > 21 and aces > 0: # aces count as 1 instead of 11
            result -= 10                # if it's beneficial for the hand
            aces -= 1
        return result

    def draw(self, surface, x1=30, y1=30, spacing=20):
        if not self.cards: return                   # continue only if there are cards
        card_w = pygame.Surface.get_width(self.cards[0].image)
        card_h = pygame.Surface.get_height(self.cards[0].image)
        for i in range(len(self.cards)):
            x = x1 + i * (spacing + card_w)
            y = y1
            self.cards[i].draw(surface, x, y)

#---------------------------------------#
class Button(object):
    """ An on-screen Pygame-based button. """
    def __init__(self, text, x, y, w=100, h=40, colouron=(0,0,0), colouroff=(5,5,255)):
        self.text = text                                        # caption
        self.rect = pygame.Rect(x, y, w, h)                     # Rect bounds
        self.colour_on = colouron                               # active colour
        self.colour_off = colouroff                             # inactive colour
        self.pressed = False                                    
        self.hovering = False                                   # mouse-over flag
        self.font = pygame.font.Font('freesansbold.ttf', 32)    # Font object
        self.font_surf = None                                   # font Surface
        self.font_rect = None                                   # font Rect bounds
        self.init_text()                                        # initialize text

    def init_text(self):
        # must be called before using the button to intialize the text
        self.font_surf = self.font.render(self.text, True, self.colour_on)
        self.font_rect = self.font_surf.get_rect()
        self.font_rect.centerx = (self.rect.left + self.rect.right) / 2
        self.font_rect.centery = (self.rect.top + self.rect.bottom) / 2

    def update(self, events):
        # determine if the mouse cursor is hovering or clicking the button
        self.hovering = self.rect.collidepoint(pygame.mouse.get_pos())
        self.pressed = False
        for event in events:
            if event.type == MOUSEBUTTONUP and self.hovering:
                self.pressed = True

    def draw(self, surface):
        # draw a button as a rectangle with text; also update the font Surface
        if self.hovering:
            pygame.draw.rect(surface, self.colour_on, self.rect, 2)
            self.font_surf = self.font.render(self.text, True, self.colour_on)
        else:
            pygame.draw.rect(surface, self.colour_off, self.rect, 2)
            self.font_surf = self.font.render(self.text, True, self.colour_off)
        # blit the text onto the game window
        surface.blit(self.font_surf, self.font_rect)
