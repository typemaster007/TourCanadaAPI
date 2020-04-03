import sys
sys.path.append('E:/Cloudproj/projects/tourcanada/')
import app
from project import app
import json
import os
from pymongo import MongoClient

import unittest 

TEST_DB = 'test.db'
UPLOAD_FOLDER = 'E:/Cloudproj/projects/tourcanada/project/view/tests'

username = "testuser1"
name = "testuser1"
email = "c@d.com"
password = "abc123"
bademail = "not@e.com"
badpassword = "notap"



class UnitTestcase(unittest.TestCase): 

    @classmethod
    def setUpClass(cls):
        username = "testuser1"
        name = "testuser1"
        email = "c@d.com"
        password = "abc123"
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
                                              # creates a test client
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(UPLOAD_FOLDER, TEST_DB)
        self.app = app.test_client()
        

    def tearDown(self):
        pass 

    def test_home_status_code(self):
        # sends HTTP GET request to the application on the specified path
        result = self.app.get('/') 
        # assert the status code of the response
        self.assertEqual(result.status_code, 302) 
        
    def test_register(self):
        a = self.app.post('/register',data=dict(username = username, name = name, email= email, password=password),follow_redirects=True)
        #print ("a =",a.data)
        b = b'{"success":true}\n'
        self.assertEqual(a.data, b)
    
    
    def test_login(self):
        a = self.app.post('/login',data=dict(email=email, password=password),follow_redirects=True)
        #print ("a2 =",a.data)
        b = b'{"success":true}\n'
        self.assertEqual(a.data, b)
        
    def test_login_failure(self):
        a = self.app.post('/login',data=dict(email=bademail, password=badpassword),follow_redirects=True)
        print ("a2 =",a.data)
        b = b'{"failure":true}\n'
        self.assertNotEqual(a.data, b)
 
#Errored out module 
#    def test_payment(self):
#        a = self.app.get('/payment',follow_redirects=True)
#        print ("a3 =",a.data)
     
#    def test_ticketgen(self):
 #     a = self.app.post('/ticketgen',data=dict(email=email, password=password),follow_redirects=True)
  #    #print ("a2 =",a.data)
   #   b = b'{"success":true}\n'
    #  self.assertEqual(a.data, b)
  

        

















     
    
        
    

    
