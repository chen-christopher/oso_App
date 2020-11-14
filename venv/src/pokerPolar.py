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
        self.cardsList = [] #A list of Card's
        self.parse(strCards)

    def parse(self, strCards):
        strCardsList = strCards.split(",")
        for strCard in strCardsList:
            number = strCard[0]
            suit = strCard[1]
            card = Card(number, suit)
            self.cardsList.append(card)

    def toNumbers(self):
        return map(lambda x: card.number, self.cardsList) 

    def toSuits(self):
        return map(lambda x: card.suit, self.cardsList) 

#HAND
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.pattern = Pattern.HighCard #The Pattern, set to the lowest by default
        self.topCards = [] #TOP 5 cards



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


#------------------CONFIG & REGISTER CLASSES----------------------
oso = Oso()
oso.register_class(Card)
oso.register_class(Cards)
oso.load_file("poker.polar")





#-------------------------FUNCTIONS---------------------------
'''
def setHand(cards): #Establish the pattern and the top 5 cards

    fiveCards = []
    pattern = Pattern.HighCard

    #POLAR QUERIES
    queryNumberCount = list(oso.query_rule("count", cards.toNumbers, Variable("elem"), Variable("count"))) 
    querySuitsCount = list(oso.query_rule("count", cards.toSuits, Variable("elem"), Variable("count")))


    #SORTING CARDS FOR NUMBER QUERY
    single = []
    pair = []
    trio = []
    quads = []

    for res in queryNumberCount:
        element = res["bindings"]["elem"]
        count = res["bindings"]["count"]

        if count == 4:
         quads.append(element)
        elif count == 3:
            trio.append(element)
        elif count == 2:
            pair.append(element)
        else:
            single.append(element)


    #SORTING CARDS FOR SUIT QUERY
    flush = None

    for res in querySuitsCount:
        element = res["bindings"]["elem"]
        count = res["bindings"]["count"]

        if count >= 5:
            flush = element




    

    #Check for straight flush in singles

    #----IMPLEMENT

    #Check for quads
    
    if len(quads) == 1:
        fiveCards.append(outputCardsWithNumber(cards, quads[0])) #Append quads
        fiveCards.append(outputCardsWithNumber(helperPokerSortDecreasing(pair + trio + single))[0]) #Append first element of sorted(singles + pair + trio)
        pattern = Pattern.Poker

    #Check for FullHouse

    if len(trio) == 2:
        sortedTrios = helperPokerSortDecreasing(sorted)
        #append three cards of sortedTrio[0] to fiveCards
        fiveCards.append(outputCardsWithNumber(sortedTrios[0]))
        #append two cards of sortedTrio[2] to fiveCards
        fiveCards.append(outputCardsWithNumber(sortedTrios[1])[:2])
        pattern = Pattern.FullHouse
    elif len(trio) == 1 and len(pair) >= 1:
        sortedPair = helperPokerSortDecreasing(pair)

        #Append three cards of trio[0]
        fiveCards.append(outputCardsWithNumber(trio[0]))
        #Append two cards of sortedPair[0]
        fiveCards.append(outputCardsWithNumber(sortedPair[0]))
        pattern = Pattern.FullHouse
    
    #Check for flush 

    if flush is not None:
        sameSuit = outputCardsWithSuit(flush)
        fiveCards = outputCardsWithNumber(helperPokerSortDecreasing(sameSuit)[:5])
        pattern = Pattern.Flush


        
    #Check for straight

    3 4 5 6 7 9 10

    1 2 3 3 4 5 7
    
    2 3 3 4 5 7 13
    
    2 3 4 5 6

    sortedOne = cards.toNumbers.sort(reverse = True)
    temp = sortedOne

    print(list(oso.query_rule("straight", sortedOne, temp)))

    #Check for Trio

    if len(trio) == 1:
        sortedSingles = helperPokerSortDecreasing(single)
        #Append three cards of trio[0] to tfiveCards
        fiveCards.append(outputCardsWithNumber(trio[0]))
        #Append sortedSingle[0 and 1] to fiveCards
        fiveCards.append(outputCardsWithNumber(sortedSingles[0]))
        fiveCards.append(outputCardsWithNumber(sortedSingles[1]))
        

    #Check for Pair

    sortedPair = helperPokerSortDecreasing(pair)

    if len(sortedPair) == 1:
        #Append sorted pair to five cards
        #Append Sorted singles three cards
    if len(sortedPair) == 2:
        #Append two sorted pair to five cards
        #Append one sorted single to five cards
    if len(sortedPair == 3):
        #Append first two sorted pair to five cards
        #singlesAndLowPair = sorted(singles + sortedPair[2])
        #Append first card of singlesAndLowPair


'''





def helperPokerSortDecreasing(list):  #Sorts in decreasing order taking into consideration 1 being the highest
    sorted = list.sort(reverse= True)
    if sorted.contains(1):
        sorted.instert(0, sorted.pop())
    return sorted


def outputCardsWithNumber(cards, number):
    return filter(lambda x: card.number == number , cards)

def outputCardsWithSuit(cards, suit):
    return filter(lambda x: card.suit == suit , cards)
    
    

temp1 = [7,5,4,3,3,2,1]
temp2 = [7,5,4,3,3,2,1]
print("STRAIGHT")
lis = list(oso.query_rule("straight", temp1, temp2, Variable("top")))
print(lis[0]['bindings']['top'])
