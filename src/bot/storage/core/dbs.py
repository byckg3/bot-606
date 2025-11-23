import redis
from pymongo import MongoClient
from pymongo.server_api import ServerApi

class MongoDB:

    def __init__( self, mongo_uri: str ):
        
        # Create a new client and connect to the server
        self.client = MongoClient( 
            mongo_uri,
            server_api = ServerApi( 
                            "1", 
                            strict = True, 
                            deprecation_errors = True ) 
        )
        self.ping()
        print( "\ncreate mongodb connection successfully" )
        
        
    def database( self, db_name: str ):
        return self.client.get_database( db_name )


    def ping( self ):
        # Send a ping to confirm a successful connection
        try:
            self.client.admin.command( "ping" )
            
        except Exception as e:
            print( e )
            
            
    def close( self ):
        # Ensures that the client will close when you finish/error
        self.client.close()
        print( "\nMongoDB connection closed." )
        

class RedisDB:

    def __init__( self, redis_uri: str ):
        self.client = redis.from_url( redis_uri )
        print( "\ncreate redis connection successfully" )
        
    def close( self ):
        self.client.close()
        print( "\nRedis connection closed." )
        
        


