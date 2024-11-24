class Caculator:
    def dmg( self, atk: int, critical_rate: float, critical_dmg: float ) -> float: 
        return atk * ( 1 + critical_rate * critical_dmg )
    
    def anomaly_dmg(  atk: int, anomaly_mastery: int ) -> float:
        return atk * anomaly_mastery / 100


# python src/bot/attributes.py
if __name__ == "__main__":
    caculator = Caculator()
    data1 = ( 1123, 0.6, 2.7 )
    print( "dmg : {}".format( caculator.dmg( *data1 ) ) )