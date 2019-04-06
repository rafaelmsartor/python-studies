from flask import Flask, jsonify, request
from flask_cors import CORS

import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask( __name__ )
CORS(app)
app.debug = True

stores = []
 
# POST - server receives data sent by the browser
# GET  - server sends data requested by the browser

# POST /store data: {name:}
@app.route( '/store', methods=['POST'] )
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append( new_store )
    return jsonify( new_store )


# GET  /store/<string:name>
@app.route( '/store/<string:name>', methods=['GET'] )
def get_store( name ):
    for store in stores:
        if store['name'] == name:
            return jsonify( store )
    return jsonify( { 'message': "Store '{}' not found!".format( name ) } )


# GET  /store
@app.route( '/store', methods=['GET'] )
def get_stores():
    return jsonify( { 'stores': stores } )


# POST /store/<string:name>/item
@app.route( '/store/<string:store_name>/item', methods=['POST'] )
def create_item_in_store( store_name ):
    request_data = request.get_json()

    for store in stores:
        if store['name'] == store_name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append( new_item )
            return jsonify( new_item )
    
    return jsonify( { 'message': "Store {} not found!".format( store_name ) } )


# GET  /store/<string:name>/item
@app.route( '/store/<string:store_name>/item', methods=['GET'] )
def get_items_in_store( store_name ):
    
    for store in stores:
        if store['name'] == store_name:
            return jsonify( { 'items': store['items'] } )
    
    return jsonify( { 'message': "Store {} not found!".format( store_name ) } )


app.run( port=5000 )