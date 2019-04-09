import sqlite3
from db import alchemy_db

class UserModel(alchemy_db.Model):

    __tablename__ = "users"
    id = alchemy_db.Column( alchemy_db.Integer, primary_key=True )
    username = alchemy_db.Column( alchemy_db.String( 80 ) )
    password = alchemy_db.Column( alchemy_db.String( 80 ) )

    def __init__( self, username, password ):
        self.username = username
        self.password = password


    def save_to_db( self ):
        alchemy_db.session.add( self )
        alchemy_db.session.commit() 

    
    @classmethod
    def find_by_username( cls, username ):
        return cls.query.filter_by( username=username ).first()


    @classmethod
    def find_by_id( cls, userid ):
        return cls.query.filter_by( id=userid ).first()


