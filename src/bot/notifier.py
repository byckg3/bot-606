import requests
from bot.crawler import Config

class DiscordNotifier:
    
    def __init__( self ):
        config = Config( "./discord_config.yaml" )
        self.webhooks = config.content[ "webhooks" ]
        self.name = "bot606"
        self.COLER_RED = 16732497
        self.COLER_GREEN = 65280
        self.COLER_BLUE = 3447003
        
    def notify_checkin_progress( self, content: dict[ str, str ] ):
        
        prefix_text = f"{ content[ "progress" ] } { content[ "checkin_status" ] }"
        match content[ "checkin_status" ]:
            case "簽到成功":
                color = self.COLER_GREEN
            case "已簽到":
                color = self.COLER_BLUE
            case _:
                color = self.COLER_RED
                prefix_text += f" [( Retry )]({ content[ 'url' ] })"
                
        notified_payload = {
            "username": self.name,
            "embeds": [
                {
                    "title": content[ "title" ],
                    "url": content[ "url" ],
                    "description": f"{ prefix_text }\n{ content[ "description" ] } ",
                    "color": color
                }
            ]
        }
        for webhook in self.webhooks:
            response = requests.post( webhook, json = notified_payload )
        
            if not response.status_code == 204:
                print( "Error: Failed to send notification." )


# python src/bot/notifier.py
if __name__ == "__main__":
    notifier = DiscordNotifier()
    notifier.notify_checkin_progress( { "test_title": "test_description" } )