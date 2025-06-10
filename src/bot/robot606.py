# from discord import Client
# import os

# class Robot606( Client ):

#     def __init__( self ):
#         super().__init__()
#         self.token_name = "DISCORD_BOT_TOKEN"
#         self._token = self._get_token()

#     def _get_token( self ):
#         token = os.getenv( self.token_name )
#         if token is None:
#             env = {}
#             with open( "env.ini" ) as file:
#                 for line in file.readlines():
#                     key, value = line.rstrip( "\n" ).split( "=" )
#                     env[ key.strip() ] = value.strip()

#             token = env[ self.token_name ]
#         return token

#     async def on_ready( self ):
#         print( "We have logged in as {0.user}".format( self ) )

#     async def on_message( self, message ):
#         print( "Message from {0.author}: {0.content}".format( message ) )

#         if message.author == self.user:
#             return

#         if message.content.startswith( "hello" ):
#             await message.channel.send( "Hi" )

#     def run( self ):
#         print( "bot is working..." )
#         return super().run( self._token )

# # python src/bot/robot606.py
# if __name__ == "__main__":
#     client = Robot606()
#     client.run()