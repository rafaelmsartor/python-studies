from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    def get( self, name ):
        item = ItemModel.find_by_name( name )

        if item:
            return item.json()

        return { 'message': 'Item not found' }, 404


    @jwt_required()
    def post( self, name ):
        if ItemModel.find_by_name( name ):
            return { 'message': "An item with name '{}' already exists.".format( name ) }, 400

        request_data = self.parse_request()

        new_item = ItemModel( name, request_data['price'], request_data['store_id'] )

        try:
            new_item.save_to_db()
        except:
            return { 'message': 'An error ocurred inserting the item.' }, 500

        return new_item.json(), 201


    @jwt_required()
    def put( self, name ):
        
        data = self.parse_request()

        item = ItemModel.find_by_name( name )
        
        if not item:
            item = ItemModel( name, data['price'], data['store_id'] )
        else:
            item.price= data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        
        return item.json()


    @jwt_required()
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

        parser.add_argument( 'store_id',
            type=int,
            required=True,
            help='Every item needs a store id'
        )

        return parser.parse_args()


class ItemsList( Resource ):

    def get( self ):
        return { 'items': [item.json() for item in ItemModel.query.all()] }