#coding:utf-8
import unittest
import os 
from work_muxixyz_app import create_app, db
from flask import current_app, url_for, jsonify
from flask_sqlalchemy import SQLALchemy
from ..work_muxixyz_app.models import Team,Group,User,Project,Message,Statu,File,Comment
import random
import json

from1 = [process,files,comments,teams] 
kind = random.ranint(1,4)
sourceID = random.ranint(1,100)

class SampleTestCase(unittest.TestCase):

    def get_api_headers(self,ifToken):
        if ifToken is True:
            return {
                'token': TOKEN,
                'Accept': 'application/json',
                'Content-Type': 'application/json'}
        else:
            return {
                'Accept': 'application/json',
                'Content-Type': 'application/json'}
    

    def setUp(self):
        self.app = create_app(
            os.getenv('FLASK_CONFIG') or 'default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.create_all()



    def test_app_exist(self):
        self.assertFalse(current_app is None)


# FEED PART

    def test_feed_a_new(self):
        response=self.client.post(
            url_for('api.signup',_external=True),
            data=json.dumps({
                "from":FROM[kind-1],
                "action":"",
                "kind":kind,
                "sourceID":sourceID}),
                headers=self.get_api_headers(False))
        self.assertTrue(response.status_code==200)



    def test_feed_b_list(self):
        response=self.client.get(
            'http://localhost/api/v1.0/feed/list/',
            headers=self.get_api_headers(True))
        self.assertTrue(response.status_code==200)
        s=json.loads(response.data.decode('utf-8'))['list']
        print (s)

#END
