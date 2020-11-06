from flask import Flask
app = Flask(__name__)



#HOME
@app.route('/')
def home():
    return 'This is Home'



#HAND
@app.route('/hand/<table_cards>/<user_cards>')
def hand(table_cards, user_cards):

    #prints on the server the input variables as example
    print(table_cards)
    print(user_cards)

    '''FIGURE OUT HAND HERE'''

    #Returns hand
    return "straight flush"

#WINNER
@app.route('/winner/<table_cards>/<int:number_users>/<users_cards>')
def winner(table_cards, number_users, users_cards):

    #prints on the server the input variables as example
    print(table_cards)
    print(number_users)
    print(users_cards)

    '''FIGURE OUT WINNER HERE'''

    #Returns winner
    return "winner is number 1"
