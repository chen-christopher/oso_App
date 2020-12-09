#IMPORTS
from flask import Flask, json
from flask_migrate import Migrate
from models import db, InfoPokerTablesModel
import pokerPolar
#--------------------CONFIG-----------------------

app = Flask(__name__)

#DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://master:master12345@database.c8ib7ubvtm2x.us-east-2.rds.amazonaws.com:5432/pokerDatabase"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app,db)
with app.app_context():
    db.create_all()



#--------------------UTILITIES----------------------
def replace_one_with_14_first_card(st):
    if (st[0] == "1") and (st[1] not in "01234"):
        new_st = "14" + st[1:]
        print(new_st)
        return new_st
    return st

def replace_one_with_14_not_first_card(st):

    return st.replace(",1H", ",14H").replace(",1D", ",14D").replace(",1S", ",14S").replace(",1C", ",14C")

def tiebreak(first_card_deck, second_card_deck):

    lis_1 = pokerPolar.convertHandtoNumbers(first_card_deck)
    lis_2 = pokerPolar.convertHandtoNumbers(second_card_deck)
    if sum(lis_1) > sum(lis_2):
        return first_card_deck
    return second_card_deck

def create_new_dict(d, rankings):
    #print(d)
    new_d = {"Rankings": rankings}
    for k in d.keys():
        st = ""
        for card in d[k].hand.topCards:
            st += str(card.number) + card.suit + ","
        new_d[str(k)] = {}
        new_d[str(k)]["Pattern"] = str(d[k].hand.pattern)
        new_d[str(k)]["Top Cards"] = st

    return new_d


#--------------------ROUTES-----------------------

#HOME
@app.route('/')
def home():
    '''
    THIS WAS AN EXAMPLE TO CHECK THE CONNECTION
    new_table = InfoPokerTablesModel(7)
    db.session.add(new_table)
    db.session.commit()'''
    return 'This is Home'



#HAND
@app.route('/hand/<table_cards>/<user_cards>')
def hand(table_cards, user_cards):

    #prints on the server the input variables as example
    deck = table_cards + user_cards
    print(user_cards)

    '''FIGURE OUT HAND HERE'''

    #Returns hand
    return "straight flush"

#WINNER
#/winner/5/4H,13H,12C,9C,5H/2H,3H;...;/
@app.route('/winner/<table_cards>/<int:number_users>/<users_cards>')
def winner(table_cards, number_users, users_cards):
    """

    INPUT: String, Int, String
    OUTPUT: {Int:{String:String, String:String}}
    Sample Input: "10H,13H,12C,9C,7H", 5, "2H,3H;5C,6C;7C,10C;9D,8D;11D,1D"

    Sample Output:
    {
        'Rankings': [0, 4, 3, 2, 1],
        0: {'Pattern': 'Pattern.Flush', 'Top Cards': '13H,10H,7H,3H,2H,'},
        1: {'Pattern': 'Pattern.HighCard', 'Top Cards': '13H,12C,10H,9C,7H,'},
        2: {'Pattern': 'Pattern.TwoPair', 'Top Cards': '10H,10C,7H,7C,13H,'},
        3: {'Pattern': 'Pattern.Pair', 'Top Cards': '9C,9D,13H,12C,10H,'},
        4: {'Pattern': 'Pattern.Straight', 'Top Cards': '14D,13H,12C,11D,10H,'}
    }





    """
    #prints on the server the input variables as example
    print(table_cards)
    print(number_users)
    print(users_cards)

    '''FIGURE OUT WINNER HERE'''
    #table_cards_as_string = ",".join(table_cards)
    cards_dict = {}
    i = 0
    #card_list = []
    users_cards = users_cards.split(";")
    print(users_cards)
    for us in users_cards:
        card_string = table_cards + "," + "".join(us)
        if ("1H" in card_string) or ("1D" in card_string) or ("1S" in card_string) or ("1C" in card_string):
            convert_first = replace_one_with_14_first_card(card_string)
            convert = replace_one_with_14_not_first_card(convert_first)


            cards_with_14 = pokerPolar.Cards(convert)
            cards_with_1 = pokerPolar.Cards(card_string)
            if cards_with_14.hand.pattern.value > cards_with_1.hand.pattern.value:
                cards_dict[i] = cards_with_14
            elif cards_with_14.hand.pattern.value < cards_with_1.hand.pattern.value:
                cards_dict[i] = cards_with_1
            else:
                cards_dict[i] = tiebreak(cards_with_14, cards_with_1)


        else:
            cards = pokerPolar.Cards(card_string) # IDK

        ### Check for aces - if 1 or 13. Then check for patterns. if higher, select the higher rank. If same rank, sum the card numbers and pick the one with the highest sum

            cards_dict[i] = cards
        i += 1

    #Returns winner
    """
    winningHand = pokerPolar.findWinner(cards_dict)
    #print(type(winningHand))
    #return winningHand
    
    
    result_as_string = "Winning Hand: \n"
    result_as_string += "PATTERN: " + str(winningHand.hand.pattern) + "\n"
    for card in winningHand.hand.topCards:

        result_as_string += str(card.number) + card.suit + "\n"
    return result_as_string

    """
    dict_copy = cards_dict.copy()
    get_winners = pokerPolar.rankedUsers(cards_dict)
    data = create_new_dict(dict_copy, get_winners)
    #print(dict_copy)
   # response = app.response_class(
   #     response=json.dumps(data),
  #      status=200,
   #     mimetype='application/json'
 #   )
    return data #pokerPolar.findWinner(cards_dict) # create_new_dict(cards_dict) #change it to winningHand

#print(winner("10H,13H,12C,9C,7H", 5, "2H,3H;5C,6C;7C,10C;9D,8D;11D,8D"))
#print(replace_one_with_14_first_card("1H,13H,12C,9C,10H,7D,1D"))
#winner/4H,13H,12C,9C,5H/5/2H,3H;5C,6C;7C,10C;9D,8D;7D,1D
#winner/10H,13H,12C,9C,7H/5/2H,3H;5C,6C;7C,10C;9D,8D;11D,8D
#print(winner("10H,13H,12C,9C,7H", 5, "2H,3H;11D,8D"))
#winner/10H,13H,12C,9C,7H/2/2H,3H;11D,8D