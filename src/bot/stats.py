import pandas as pd
import matplotlib.pyplot as plt

class Caculator:
    
    def __init__( self, stats: dict ):
        self.atk = stats.get( "atk", 1000 )
        self.critical_rate = stats.get( "cr", 0.05 )
        self.critical_dmg = stats.get( "cd", 0.5 )
        self.penetration_ratio = stats.get( "pen_ratio", 0 )
        self.penetration_value = stats.get( "pen_value", 0 )
        self.anomaly_mastery = stats.get( "am", 100 )
        
    def defense_multiplier( self ):
        lv = 60
        target_def = 100
        reduced_def_ratio = 0
        def_factor = target_def * ( 1 - reduced_def_ratio ) * ( 1 - self.penetration_ratio ) - self.penetration_value
        multiplier = lv / ( lv + def_factor )
        
        return round( multiplier, 3 )
    
    def base_multiplier( self ):
        return self.atk * self.defense_multiplier()
         
    def dmg( self, bonus_multiplier: float = 0 ) -> float: 
        return self.base_multiplier() * ( 1 + self.critical_rate * self.critical_dmg ) * ( 1 + bonus_multiplier )
    
    def anomaly_dmg( self, atk: int, bonus_multiplier: float = 0 ) -> float:
        return self.base_multiplier() * self.anomaly_mastery / 100 * ( 1 + bonus_multiplier )


# python src/bot/stats.py
if __name__ == "__main__":
   
    stats1 = { "atk": 2976, "cr": 0.858, "cd": 1.364 } 
    stats2 = { "atk": 3452 + 631, "cr": 1, "cd": 1.46 }
    
    role1 = Caculator( stats1 )
    role2 = Caculator( stats2 )
    
    bonus_multipliers = [ 0.35, 0.55, 0.65, 0.85, 1.05 ]
    
    print( "dmg1 : {:.2f}".format( role1.dmg( 1.05 ) ) )
    print( "dmg2 : {:.2f}".format( role2.dmg( 0.35 ) ) )
    
    data = { "multiplier": bonus_multipliers, 
             "dmg1": [ role1.dmg( y1 ) for y1 in bonus_multipliers ],
             "dmg2": [ role2.dmg( y2 ) for y2 in bonus_multipliers ] }
    
    df = pd.DataFrame( data )
    df.plot.bar( x = "multiplier", y = [ "dmg1", "dmg2" ], rot = 0, grid = True )
    # df.plot( x = "multiplier", y = [ "dmg1", "dmg2" ], kind = "bar", title = "Line Chart" ) 
    
    plt.show()