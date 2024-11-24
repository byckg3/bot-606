class Caculator:
    def dmg( self, atk: int, critical_rate: float, critical_dmg: float, bonus_multiplier: float = 0 ) -> float: 
        return atk * ( 1 + critical_rate * critical_dmg ) * ( 1 + bonus_multiplier )
    
    def anomaly_dmg(  atk: int, anomaly_mastery: int, bonus_multiplier: float = 0 ) -> float:
        return atk * anomaly_mastery / 100 * ( 1 + bonus_multiplier )


# python src/bot/stats.py
if __name__ == "__main__":
    caculator = Caculator()
    data1 = ( 2976, 0.858, 1.364, 1.05 )
    print( "dmg : {:.2f}".format( caculator.dmg( *data1 ) ) )
    
    data2 = ( 3452 + 631, 1, 1.46, 0.35 )
    print( "dmg : {:.2f}".format( caculator.dmg( *data2 ) ) )