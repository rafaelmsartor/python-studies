import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__( self, userid, username, password ):
        self.id = userid
        self.username = username
        self.password = password    

    
    @classmethod
    def find_by_username( cls, username ):
        connection =  sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute( query, (username,) )
        row = result.fetchone()

        if row:
            user = cls( *row )
        else:
            user = None
        
        connection.close()
        return user


    @classmethod
    def find_by_id( cls, userid ):
        connection = sqlite3.connect( 'data.db' )
        cursor = connection.cursor()

        query = "SELECT * FROM users where id=?"
        result = cursor.execute( query, (userid,) )
        row = result.fetchone()

        if row:
            user = cls( *row )
        else:
            user = None

        connection.close()
        return user



class UserRegister( Resource ):
    parser = reqparse.RequestParser()

    parser.add_argument( 'username',
        type=str,
        required=True
    )

    parser.add_argument( 'password', 
        type=str,
        required=True,
    )
        

    def post( self ):
        data =  UserRegister.parser.parse_args()

        if User.find_by_username( data['username'] ):
            return { 'message': 'That username is already in use' }, 400

        if not data:
            return { 'message': 'Username or password missing.' }, 400

        connection = sqlite3.connect()
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES( NULL, ?, ? )"
        cursor.execute( query, data['username'], data['password'] )

        connection.commit()
        connection.close()

        return { 'message': 'User created successfully.' }, 201