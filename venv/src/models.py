from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InfoPokerTablesModel(db.Model):
    __tablename__ = 'tables_registered'

    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String())
    number_users = db.Column(db.Integer)

    def __init__(self, number_users ):
        self.code = '127'
        self.number_users = number_users