import requests
from bot.crawler import Config

class DiscordNotifier:
    
    def __init__( self ):
        config = Config( "./discord_config.yaml" )
        
        self.webhooks = config.content[ "webhooks" ]
        
    def notify( self, title: str, description: str, url: str = None ):
        
        payload = {
            "username": "bot606",
            "embeds": [
                {
                    "title": title,
                    "url": url,
                    "description": description,
                    "color": 3447003
                }
            ]
        }
        for webhook in self.webhooks:
            response = requests.post( webhook, json = payload )
        
            if not response.status_code == 204:
                print( "error occur!!" ) 
           
            print( f"HTTP status code: { response.status_code }" )


# python src/bot/notifier.py
if __name__ == "__main__":
    notifier = DiscordNotifier()
    notifier.notify( "test_title", "test_description" )