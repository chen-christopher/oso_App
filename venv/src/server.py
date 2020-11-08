from flask import Flask
from flask_migrate import Migrate
from models import db, InfoPokerTablesModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://master:master12345@database.c8ib7ubvtm2x.us-east-2.rds.amazonaws.com:5432/pokerDatabase"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app,db)

with app.app_context():
    db.create_all()


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
