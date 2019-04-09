from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

from models.item import ItemModel

class Item(Resource):
    @jwt_required()
    def get( self, name ):
        item = ItemModel.find_by_name( name )

        if item:
            return item.json()

        return { 'message': 'Item not found' }, 404


    def post( self, name ):
        if ItemModel.find_by_name( name ):
            return { 'message': "An item with name '{}' already exists.".format( name ) }, 400

        request_data = self.parse_request()

        new_item = ItemModel( name, request_data['price'] )

        try:
            new_item.save_to_db()
        except:
            return { 'message': 'An error ocurred inserting the item.' }, 500

        return new_item.json(), 201


    def put( self, name ):
        
        data = self.parse_request()

        item = ItemModel.find_by_name( name )
        
        if not item:
            item = ItemModel( name, data['price'] )
        else:
            item.price= data['price']

        item.save_to_db()
        
        return item.json()


    def delete( self, name ):
        item = ItemModel.find_by_name( name )

        if item:
            item.delete_from_db()
        
        return { 'message': 'Item deleted' }


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
       
        items = []

        for row in result:
            items.append( {
                'name' : row[0],
                'price': row[1]
            })
        
        connection.close()

        return { 'items': items }