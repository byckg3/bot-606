import pandas as pd
import matplotlib.pyplot as plt

class Caculator:
    def dmg( self, atk: int, critical_rate: float, critical_dmg: float, bonus_multiplier: float = 0 ) -> float: 
        return atk * ( 1 + critical_rate * critical_dmg ) * ( 1 + bonus_multiplier )
    
    def anomaly_dmg( self, atk: int, anomaly_mastery: int, bonus_multiplier: float = 0 ) -> float:
        return atk * anomaly_mastery / 100 * ( 1 + bonus_multiplier )


# python src/bot/stats.py
if __name__ == "__main__":
    caculator = Caculator()
    
    stats1 = ( 2976, 0.858, 1.364 )
    stats2 = ( 3452 + 631, 1, 1.46 )
    multipliers = [ 0.35, 0.55, 0.65, 0.85, 1.05 ]
    
    print( "dmg : {:.2f}".format( caculator.dmg( *stats1, 1.05 ) ) )
    print( "dmg : {:.2f}".format( caculator.dmg( *stats2, 0.35 ) ) )
    
    data = { "multiplier": multipliers, 
             "dmg1": [ caculator.dmg( *stats1, y1 ) for y1 in multipliers ],
             "dmg2": [ caculator.dmg( *stats2, y2 ) for y2 in multipliers ] }
    
    df = pd.DataFrame( data )
    df.plot.bar( x = "multiplier", y = [ "dmg1", "dmg2" ], rot = 0, grid = True )
    # df.plot( x = "multiplier", y = [ "dmg1", "dmg2" ], kind = "bar", title = "Line Chart" ) 
    
    plt.show()