#IMPORTS
from flask import Flask
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

    #prints on the server the input variables as example
    print(table_cards)
    print(number_users)
    print(users_cards)

    '''FIGURE OUT WINNER HERE'''
    #table_cards_as_string = ",".join(table_cards)
    card_list = []
    users_cards = users_cards.split(";")
    print(users_cards)
    for us in users_cards:
        card_string = table_cards + "," + "".join(us)
        card = pokerPolar.Cards(card_string) # IDK
        ### Check for aces - if 1 or 13
        card_list.append(card)

    #Returns winner
    winningHand = pokerPolar.findWinner(card_list)
    #print(type(winningHand))
    #return winningHand
    result_as_string = "Winning Hand: \n"
    result_as_string += "PATTERN: " + str(winningHand.hand.pattern) + "\n"
    for card in winningHand.hand.topCards:

        result_as_string += str(card.number) + card.suit + "\n"
    return result_as_string



#print(winner("4H,13H,12C,9C,5H", 5, "2H,3H;5C,6C;7C,10C;9D,8D;7D,1D"))

#winner/4H,13H,12C,9C,5H/5/2H,3H;5C,6C;7C,10C;9D,8D;7D,1D

