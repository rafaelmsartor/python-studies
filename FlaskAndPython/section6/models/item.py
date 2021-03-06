import sqlite3
from db import alchemy_db

class ItemModel(alchemy_db.Model):

    __tablename__ = "items"
    id = alchemy_db.Column( alchemy_db.Integer, primary_key=True )
    name = alchemy_db.Column( alchemy_db.String( 80 ) )
    price = alchemy_db.Column( alchemy_db.Float( precision=2 ) )

    store_id = alchemy_db.Column( alchemy_db.Integer, alchemy_db.ForeignKey('stores.id') )
    store = alchemy_db.relationship( 'StoreModel' )


    def __init__( self, name, price, store_id ) :
        self.name = name
        self.price = price
        self.store_id = store_id


    def json( self ):
        return { 
            'name': self.name,
            'price': self.price
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
        