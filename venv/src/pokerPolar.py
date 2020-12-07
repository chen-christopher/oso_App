from oso import Oso
from oso import Variable
import enum




#-----------------------------CLASSES--------------------------

#CARD CLASS
class Card:
	def __init__(self, number, suit):
		self.number = number
		self.suit = suit
		#self.suit_numeric = 0



#TOTAL CARDS CLASS: USERS CARDS + DEALERS CARDS
class Cards:
	def __init__(self, strCards): #strCards is in the following format : "1H,2D,4H" it can be uo to 7 cards in total
		self.cardsList = [] #A list of Card's
		self.parse(strCards)
		self.hand: Hand

	def parse(self, strCards):
		strCardsList = strCards.split(",")
		number = 0
		suit = ""
		for strCard in strCardsList:
			if (("10" in strCard) or ("11" in strCard) or ("12" in strCard) or ("13" in strCard) or ("14" in strCard)):
					number = int(strCard[0] + strCard[1])
					suit = strCard[2]
			else:
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
oso.register_class(Pattern)
oso.load_file("poker.polar")

def setHand(cards): #Establish the pattern and the top 5 cards

	#fiveCards = []
   list_of_all_cards = cards
   list_of_all_faces = toNumbers(cards)
   list_of_all_suits = toSuits(cards)
   duplicate_list_of_all_faces = toNumbers(cards)
   top_cards = []
   pattern = 0 #: Pattern
   check_for_flush = ""
   polar_result = list(oso.query_rule("hand", list_of_all_cards, list_of_all_faces, duplicate_list_of_all_faces, list_of_all_suits, Variable("result")))
	#POLAR QUERIES
   if len(polar_result) > 0:
	   #print(polar_result)
	   result = polar_result[0]["bindings"]["result"]
	   for i in range(len(result)):
		   if i == 0:
			   pattern = result[i]
			   #print(pattern)
			   check_for_flush = str(pattern)
			   #print(check_for_flush)
		   else:
			   top_cards.append(result[i])
			   #print("(" + str(result[i].number) + "," + result[i].suit + ")" + "\n")

			
   else:
	   print("Unexpected Error occurred while running the Poker Hand Analyzer")		
	   return Hand(cards, Pattern.HighCard, top_cards)

   if "Pattern.Flush" == check_for_flush:

	   def sort_flush(x):
		    return x.number

	   top_cards.sort(key = sort_flush, reverse=True)

   return Hand(cards, pattern, top_cards)

#-------------------------FUNCTIONS---------------------------
"""
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
		


"""




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
	print(top)
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


#<<<<<<< Updated upstream
def straightHelper(numbers):
	temp1 = numbers.copy()
	temp2 = numbers.copy()

	straightQuery = list(oso.query_rule("straight", temp1, temp2, Variable("top")))
	if len(straightQuery) == 0:
		return 0
	else:
		return straightQuery[0]['bindings']['top']


def convertHandtoNumbers(cards):
	cardList = []
	for card in cards.hand.topCards:
		cardString = card.number
		cardList.append(cardString)
	return cardList


def findWinner(allHands):
	winningHand = None
	winningHandScore = 0
	for thisHand in allHands:
		thisHandScore = thisHand.hand.pattern.value
		# If the pattern match of this hand is greater than the current winner, set this hand as new best
		if thisHandScore > winningHandScore:
			winningHand = thisHand
			winningHandScore = thisHandScore
		# If the pattern match of this hand is the same as the current winner, do high card comparison
		elif(thisHandScore == winningHandScore):
			thisCard, oldCard = None, None
			thisHandList = convertHandtoNumbers(thisHand)
			oldHandList = convertHandtoNumbers(winningHand)
			for thisCard, oldCard in zip(thisHandList, oldHandList):
				if thisCard != oldCard:
					break
			if thisCard > oldCard:
				winningHand = thisHand.hand
				winningHandScore = thisHandScore

	print(type(winningHand))
	print("WINNING HAND: ")
	for card in winningHand.hand.topCards:
		print(str(card.number) + card.suit)
	return winningHand


#TEST

#hand1 = Cards("1H,2H,4D,2D,3D,5H")
#hand2 = Cards("1H,1D,4D,1T,2C,4H,2H")
#hand3 = Cards("13C,8C,1H,6H,4H,3H,2H")

#hand4 = Cards("4H,5D,4C,2H,2D,3C,3H")
#hand5 = Cards("2H,3H,4H,5H,6H,7H")
#hand6 = Cards("3D,3H,2H,3C,2D,3S,1S")
#hand7 = Cards("13H,3H,2C,3D,13S,9C,13C")

#allHands = [hand1, hand2, hand3, hand4, hand5]

#findWinner(allHands)
#=======
"""
temp1 = [7,5,4,3,3,2,1]
temp2 = [7,5,4,3,3,2,1]

temp3 = [3, 6, 7, 3, 4, 8, 2]
temp4 = [3, 7, 6, 5, 4, 3, 2]
temp5 = [3, 10, 5, 6, 4, 3, 2]
#print("STRAIGHT")
#lis = list(oso.query_rule("pair", temp3, Variable("v")))
#lis = list(oso.query_rule("straight", temp4, temp5, Variable("top")))
#print(lis[0]['bindings']['top'])
#print(lis)

#lis_2 = list(oso.query_rule("samp", temp1, Variable("v")))
#print(lis_2)
card1 = Card(2, "H") # Card(2, "H")
card2 = Card(13, "H")
card3 = Card(6, "S")
card4 = Card(8, "D")
card5 = Card(10, "H")
card6 = Card(8, "C")
card7 = Card(1, "H")
check_lis = [7, 6, 2, 4, 2, 7, 7]
#temp9 = [card1, card2, card3, card4, card5, card6, card7]
#temp10 = [card1.number, card2.number, card3.number, card4.number, card5.number, card6.number, card7.number] # for checking
temp11 = [card1.number, card2.number, card3.number, card4.number, card5.number, card6.number, card7.number] # for iteration
temp9 = [card1, card2, card3, card4, card5, card6, card7]
temp10 = [card1.number, card2.number, card3.number, card4.number, card5.number, card6.number, card7.number]

temp13 = [card1.number, card2.number, card3.number, card4.number]
temp12 = [card1.suit, card2.suit, card3.suit, card4.suit, card5.suit, card6.suit, card7.suit]
#temp12 = [card1.number, card2.number, card3.number, card4.number]
v = 6 
temp14 = [1,1,2,2]






"""

#temp12 = ["h", "c", "h", "d"]
#lis = list(oso.query_rule("same", temp10, v, Variable("card1"), temp11))
#lis = list(oso.query_rule("max_of_remaining_cards", temp10, temp11, temp12, Variable("card")))
#lis = list(oso.query_rule("max_util", card6, temp10, temp12, Variable("card")))
#max_of_remaining_cards(list_of_all_faces, [head, *tail], list_of_seen_cards_faces, card)
#lis = list(oso.query_rule("max_of_remaining_cards", temp10, temp9, temp12, Variable("card")))
#print(lis)
#oso.register_class(Pattern)
#oso.register_class(Card)
#lis = list(oso.query_rule("four_of_a_kind", temp9, temp10, Variable("result")))
#lis = list(oso.query_rule("flush", temp9, temp12, Variable("result")))
#lis = list(oso.query_rule("straight_flush", temp9, temp10, temp11, temp12, Variable("result")))
#lis = list(oso.query_rule("hand", temp9, temp10, temp11, temp12, Variable("result")))
#c#ard_list = []
#pattern: Pattern
"""
lis = list(oso.query_rule("three", check_lis, Variable("v")))
if (len(lis) > 0):
	print(lis)
else:
	print("Error")
"""
#if len(lis) > 0:
	#print(lis[0]["bindings"]["card"].number, " ", lis[0]["bindings"]["card"].suit)
#	print(lis)
	#print(lis[0]["bindings"]["result"][0].number, " ", lis[0]["bindings"]["card"].suit)
#	result = lis[0]["bindings"]["result"]
#	for i in range(len(result)):
#		if i == 0:
#			pattern = result[i]
#			print(pattern)
#		else:
#			card_list.append(result[i])
#			print("(" + str(result[i].number) + "," + result[i].suit + ")" + "\n")

			
#else:
#	print("error")		

#>>>>>>> Stashed changes
#lis = list(oso.query_rule("samp", temp14, 1))
 

























