from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    @jwt_required()
    def get( self, name ):
        item = self.find_by_name( name )

        if item:
            return item

        return { 'message': 'Item not found' }, 404


    def post( self, name ):
        if self.find_by_name( name ):
            return { 'message': "An item with name '{}' already exists.".format( name ) }, 400

        request_data = self.parse_request()

        new_item = {
            'name': name,
            'price': request_data['price']
        }

        try:
            self.insert( new_item )
        except:
            return { 'message': 'An error ocurred inserting the item.' }, 500

        return new_item, 201


    def put( self, name ):
        
        data = self.parse_request()

        item = self.find_by_name( name )
        updated_item = { 'name': name, 'price': data['price'] }
            
        if not item:
            try:
                self.insert( updated_item )
            except:
                return { 'message': 'An error ocurred while inserting the item.' }
        else:
            try:
                self.update( updated_item )
            except:
                return { 'message': 'An error ocurred while updating the item.' }
        
        return updated_item


    def delete( self, name ):
        connection = sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute( query, (name,) )
        connection.close()
        
        return { 'message': 'Item deleted' }
        

    @classmethod
    def find_by_name( cls, name ):
        connection = sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute( query, (name,) )
        row = result.fetchone()

        connection.close()

        if row:
            return { 'name': row[0], 'price': row[1] }

        return None


    @classmethod
    def insert( cls, item ):
        connection = sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute( query, ( item['name'], item['price'] ) )

        connection.commit()
        connection.close()


    @classmethod
    def update( cls, item ):
        connection = sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute( query, (item['price'], item['name'] ) )

        connection.commit()
        connection.close()


    @staticmethod
    def parse_request():
        parser = reqparse.RequestParser()

        parser.add_argument( 'price',
            type=float,
            required=True,
            help='This argument must not be empty'
        )

        return parser.parse_args()


class ItemsList( Resource ):

    def get( self ):
        connection = sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute( query )
        connection.close()

        items = []

        for row in result:
            items.append( {
                'name' : row[0],
                'price': row[1]
            })

        return { 'items': items }