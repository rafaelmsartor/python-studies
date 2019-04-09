import sqlite3
from db import alchemy_db

class ItemModel(alchemy_db.Model):

    __tablename__ = "items"
    id = alchemy_db.Column( alchemy_db.Integer, primary_key=True )
    name = alchemy_db.Column( alchemy_db.String( 80 ) )
    price = alchemy_db.Column( alchemy_db.Float( precision=2 ) )


    def __init__( self, name, price ) :
        self.name = name
        self.price = price


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


    def update( self ):
        connection = sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute( query, ( self.price, self.name ) )

        connection.commit()
        connection.close()

    
    def delete_from_db( self ):
        alchemy_db.session.delete( self )
        alchemy_db.session.commit()
        