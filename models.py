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



##################

"""
Register{
    id: asjahsjahskakdjak7&^^FVUV@
    code: 1231223 #Kahoot Code
    startTime: "2020,12,11,5PM"
    smallBlind: 10
    bigBlind: 20
    maxNumberParticipants: 6
    numberParticipants: 5
    initialMoney: 1000
    paricipantsIDs: {0: 1231231, 1: 1231244, 2: 1251353, 3: 113515,4: 13135135}
    participantsUsername: {1231231: Mozart,1231244: Bach,1251353: Linus,113515: Plato,13135135: Socrates}
    paritcipantsCurrentMoney: {1231231: 1230,1231244: 2000,1251353: 350,113515: Plato,200: 835}
    BigBlindPosition: 2
    NumberOfPlays: 45
    NumberOfActions: 125


}

Round{
    id: jashdahsjkdhasd7haksjdhj3
    tableId: asjahsjahskakdjak7&^^FVUV@ #LINKED WITH REGISTER ID
    participantsCars: {1231231: 2H3D,1231244: 8H7D,1251353: 2T3C,113515: 4H1D,13135135: 2H3D}
    tableCars: [2h, 5h, 10D]
    
}


Action{
    id: kajskjas8j3j3j3ju
    roundId: jashdahsjkdhasd7haksjdhj3&
    tableId: asjahsjahskakdjak7&^^FVUV@ 
    playersTurn: 2
    action: Bet #options: BET, FOLD, CALL, CHECK
    bet: 200
    call: NULL
 
}
"""



