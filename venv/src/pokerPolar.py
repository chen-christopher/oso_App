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
        self.hand: Hand

    def parse(self, strCards):
        strCardsList = strCards.split(",")
        for strCard in strCardsList:
            number = int(strCard[0])
            suit = strCard[1]
            card = Card(number, suit)
            self.cardsList.append(card)
        self.hand = setHand(self.cardsList)
        self.hand.output()

#HAND
class Hand:
    def __init__(self, cards, pattern, topCards):
        self.cards = cards
        self.pattern = pattern
        self.topCards = topCards
    
    def output(self):
        print("PATTERN: " + str(self.pattern))
        print("TOP CARDS:")
        for card in self.topCards:
            print(str(card.number) + card.suit)



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

def setHand(cards): #Establish the pattern and the top 5 cards
    
    fiveCards = []

    #POLAR QUERIES
    queryNumberCount = list(oso.query_rule("count", toNumbers(cards), Variable("elem"), Variable("count"))) 
    querySuitsCount = list(oso.query_rule("count", toSuits(cards), Variable("elem"), Variable("count")))

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

    
   


    #CHECK FOR HAND HIERARCHY CASCADE

    #Check for straight flush 

    if flush is not None:
        sameSuit = outputCardsWithSuit(cards, flush)
        straightcards = checkForStraight(sameSuit)
        
        if len(straightcards) > 0:
            fiveCards = straightcards
            pattern = Pattern.StraightFlush
            return Hand(cards, pattern, fiveCards)

    

    #Check for quads
    
    if len(quads) == 1:
        fiveCards += outputCardsWithNumber(cards, quads[0]) #Append quads
        join = pair + trio + single
        fiveCards.append(outputCardsWithNumber(cards, helperPokerSortDecreasing(join)[0])[0]) #Append first element of sorted(singles + pair + trio)
        pattern = Pattern.Poker
        return Hand(cards, pattern, fiveCards)

    #Check for FullHouse

    if len(trio) == 2:
        sortedTrios = helperPokerSortDecreasing(trio)
        #append three cards of sortedTrio[0] to fiveCards
        fiveCards += outputCardsWithNumber(cards, sortedTrios[0])
        #append two cards of sortedTrio[2] to fiveCards
        fiveCards += outputCardsWithNumber(cards, sortedTrios[1])[:2]
        pattern = Pattern.FullHouse
        return Hand(cards, pattern, fiveCards)
    if len(trio) == 1 and len(pair) >= 1:
        sortedPair = helperPokerSortDecreasing(pair)

        #Append three cards of trio[0]
        fiveCards += outputCardsWithNumber(cards, trio[0])
        #Append two cards of sortedPair[0]
        fiveCards += outputCardsWithNumber(cards, sortedPair[0])
        pattern = Pattern.FullHouse
        return Hand(cards, pattern, fiveCards)
    
    #Check for flush 

    if flush is not None:
        sameSuit = toNumbers(outputCardsWithSuit(cards, flush))
        sameSuit = helperPokerSortDecreasing(sameSuit)
        for number in sameSuit:
            fiveCards.append(outputCardsWithNumber(cards, number)[0])
        fiveCards = fiveCards[:5]
        pattern = Pattern.Flush
        return Hand(cards, pattern, fiveCards)


        
    #Check for straight

    straightCards = checkForStraight(cards)
    if len(straightCards) != 0:
            fiveCards = straightCards
            pattern = Pattern.Straight
            return Hand(cards, pattern, fiveCards)


    #Check for Trio

    if len(trio) == 1:
        sortedSingles = helperPokerSortDecreasing(single)
        #Append three cards of trio[0] to tfiveCards
        fiveCards += outputCardsWithNumber(cards, trio[0])
        #Append sortedSingle[0 and 1] to fiveCards
        fiveCards += outputCardsWithNumber(cards, sortedSingles[0:2])
        pattern = Pattern.Trio
        return Hand(cards, pattern, fiveCards)
        

    #Check for Pair

    sortedPair = helperPokerSortDecreasing(pair)
    sortedSingles = helperPokerSortDecreasing(single)
    if len(sortedPair) == 1:
        #Append sorted pair to five cards
        fiveCards += outputCardsWithNumber(cards, sortedPair[0])
        #Append Sorted singles three cards
        fiveCards += outputCardsWithNumber(cards, sortedSingles[0:3])
        pattern = Pattern.Pair
        return Hand(cards, pattern, fiveCards)

    if len(sortedPair) == 2:
        #Append two sorted pair to five cards
        sortedPair = helperPokerSortDecreasing(pair)
        fiveCards += outputCardsWithNumber(cards, sortedPair[0])
        fiveCards += outputCardsWithNumber(cards, sortedPair[1])
        #Append one sorted single to five cards
        fiveCards.append(outputCardsWithNumber(cards, sortedSingles[0])[0])
        pattern = Pattern.TwoPair
        return Hand(cards, pattern, fiveCards)
    if len(sortedPair) == 3:
        #Append first two sorted pair to five cards
        sortedPair = helperPokerSortDecreasing(pair)
        fiveCards += outputCardsWithNumber(cards, sortedPair[0])
        fiveCards += outputCardsWithNumber(cards, sortedPair[1])
        #Append first card of singlesAndLowPair
       
        singlesAndLowPair = helperPokerSortDecreasing(sortedSingles + [sortedPair[2]])
        fiveCards.append(outputCardsWithNumber(cards, singlesAndLowPair[0])[0])
        pattern = Pattern.TwoPair
        return Hand(cards, pattern, fiveCards)

    
    #HighCards
    fiveCards = sortedSingles[0:5]
    pattern = Pattern.HighCard
    return Hand(cards, pattern, fiveCards) 
        







def toNumbers(cards):
    numbers = []
    for card in cards:
        numbers.append(card.number)
    return numbers

def toSuits(cards):
    suits = []
    for card in cards:
        suits.append(card.suit)
    return suits


def helperPokerSortDecreasing(numbers):  #Sorts in decreasing order taking into consideration 1 being the highest
    ones = []
    rest =[]
    for number in numbers:
        if number == 1:
            ones.append(number)
        else:
            rest.append(number)
    rest.sort(reverse= True)
    final = ones + rest
    return final


def outputCardsWithNumber(cards, number):
    newCards = []
    for card in cards:
        if card.number == number:
            newCards.append(card)
    return newCards
    

def outputCardsWithSuit(cards, suit):
    newCards = []
    for card in cards:
        if card.suit == suit:
            newCards.append(card)
    return newCards

def checkForStraight(cards):
    uniqueNumbers = []
    uniqueCards = []
    for card in cards:
        if card.number not in uniqueNumbers:
            uniqueNumbers.append(card.number)
            uniqueCards.append(card)
    if (len(uniqueNumbers) < 5):
        return []
        
    firstArray = uniqueNumbers
    firstArray.sort(reverse = True)
    secondArray = []
    for number in uniqueNumbers:
        if number == 1:
            secondArray.append(13)
        else:
            secondArray.append(number)
    top = max(straightHelper(firstArray), straightHelper(secondArray))
    if top == 0:
        return []
    
    sortedCards = []

    index = 0
    while (index < 5):
        number = top - index
        if (number == 13):
            number = 1
        card = outputCardsWithNumber(uniqueCards, number)[0]
        sortedCards.append(card)
        index += 1
    return  sortedCards
    

def straightHelper(numbers):
    temp1 = numbers.copy()
    temp2 = numbers.copy()
    
    straightQuery = list(oso.query_rule("straight", temp1, temp2, Variable("top")))
    if len(straightQuery) == 0:
        return 0
    else:
        return straightQuery[0]['bindings']['top']





    
    

#TEST

cards = Cards("1H,2H,4D,2D,3D,5H")
cards = Cards("1H,1D,4D,1T,1C,5H")
cards = Cards("5H,1D,4D,1T,4C,5H")



"1H,2H,4D,2D,3D,5H,8C"

pattern = straight
topFiveCards = 1H, 2H, 3D, 4D, 5H


"5H,1D,4D,1T,4C,5C, 9C"

pattern = two pair


1D, 1C, 1T, 4H, 5H, 6H, 8H

1D, 1C, 1T, 8, 6


2,3,4,5,6,7,8,9,10,J,Q,K,A