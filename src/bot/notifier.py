import requests
from bot.crawler import Config

class DiscordNotifier:
    
    def __init__( self ):
        config = Config( "./discord_config.yaml" )
        
        self.webhooks = config.content[ "webhooks" ]
        self.COLER_RED = 16711680
        self.COLER_GREEN = 65280
        self.COLER_BLUE = 3447003
        
    def notify( self, **kwargs ):
        
        color = self.COLER_RED
        match kwargs[ "state" ]:
            case "簽到成功":
                color = self.COLER_GREEN
            case "已簽到":
                color = self.COLER_BLUE
                
        payload = {
            "username": "bot606",
            "embeds": [
                {
                    "title": kwargs[ "title" ],
                    "url": kwargs[ "url" ],
                    "description": f"{ kwargs[ "progress" ] } { kwargs[ "state" ] }\n{ kwargs[ "description" ] } ",
                    "color": color
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