'''
Created on Jul 3, 2018

@author: afm
'''
import unittest
import logging

class Test(unittest.TestCase):

    def setUp(self):
        print(time)
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(funcName)s: %(message)s',
                    level=logging.DEBUG)
        

    def tearDown(self):
        pass

#     def timezone_offset_seconds(self,server_info):
#         '''
#         This is a copy from topsServe_rollmonitor, because i want to make sure
#         if that one gets modified and breaks, this ones doesn't. 
#         
#         Convert the timezone string in server_info into a signed integer of seconds.