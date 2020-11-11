from oso import Oso
from oso import Variable
import enum




#-----------------------------CLASSES--------------------------

#CARD CLASS
class Card:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit


#TOTAL CARDS CLASS: USERS CARDS + DEALERS CARDS
class Cards:
    def __init__(self, strCards): #strCards is in the following format : "1H,2D,4H" it can be uo to 7 cards in total
        self.cardsList = [] #An list of Card's
        self.parse(strCards)

    def parse(self, strCards):
        strCardsList = strCards.split(",")
        for strCard in strCardsList:
            number = strCard[0]
            suit = strCard[1]
            card = Card(number, suit)
            self.cardsList.append(card)

#HAND
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.pattern = self.findPattern(cards) #The Pattern, set to the lowest by default
        self.topCards = [] #TOP 5 cards
    
    def findPattern(self, cards):
        return Pattern.HighCard


    def findTopCards(self, cards, pattern):
        return


#PATTERN
class Pattern(enum.Enum):
    HighCard = 1
    Pair = 2
    TwoPair = 3
    Trio = 4
    Straight = 5
    Flush = 6
    FullHouse = 7
    Poker = 8
    StraightFlush = 9


#------------------ONFIG & REGISTER CLASSES----------------------
oso = Oso()
oso.register_class(Card)
oso.register_class(Cards)
oso.load_file("poker.polar")

print(list(oso.query_rule("count", [1,2,3,4,1,2], Variable("elem"), Variable("count"))))


        
