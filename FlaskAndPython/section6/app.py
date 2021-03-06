from flask import Flask 
from flask_restful import Api
from flask_jwt import JWT 

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemsList
from resources.store import Store, StoreList

app = Flask( __name__ )

app.secret_key = "MySuperAwesomeSecretKey"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

api = Api( app )

jwt = JWT( app, authenticate, identity ) # /auth

@app.before_first_request
def create_tables():
    alchemy_db.create_all()

api.add_resource( Item, '/item/<string:name>' )
api.add_resource( ItemsList, '/items' )
api.add_resource( UserRegister, '/register')
api.add_resource( Store, '/store/<string:name>')
api.add_resource( StoreList, '/stores')

if __name__ == '__main__':
    from db import alchemy_db
    alchemy_db.init_app ( app )
    app.run( port=5000, debug=True )
