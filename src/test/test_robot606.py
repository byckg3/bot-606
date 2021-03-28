import unittest, sys
sys.path.insert( 0, "./src" )

from bot import Robot606

# python -m unittest src/test/test_robot606.py -v
class Robot606Tests( unittest.TestCase ):

    def setUp( self ):
        self.client = Robot606()

    def test_get_token( self ):
        self.assertTrue( self.client._token )