import sqlite3
from db import alchemy_db

class StoreModel(alchemy_db.Model):

    __tablename__ = "stores"
    id = alchemy_db.Column( alchemy_db.Integer, primary_key=True )
    name = alchemy_db.Column( alchemy_db.String( 80 ) )
   
    items = alchemy_db.relationship( 'ItemModel', lazy='dynamic' )
   
    def __init__( self, name ) :
        self.name = name
        


    def json( self ):
        return { 
            'name': self.name,
            'items': [item.json for item in self.items.all()]
        }

    
    @classmethod
    def find_by_name( cls, name ):
        return cls.query.filter_by( name=name ).first() # SELECT * FROM items WHERE name=name LIMIT 1


    def save_to_db( self ):
        alchemy_db.session.add( self )
        alchemy_db.session.commit()


    def delete_from_db( self ):
        alchemy_db.session.delete( self )
        alchemy_db.session.commit()
        