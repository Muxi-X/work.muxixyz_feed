'''coding = utf-8'''
import unittest
import os
import random
import json
from flask import current_app, url_for, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
from work_muxixyz_app import create_app, db
from work_muxixyz_app.models import Team, User, Group, Project, Message, Statu, File, Comment, User2Project

#db = SQLAlchemy()
FROM = ['process', 'files', 'comments', 'teams']
KIND = random.randint(1, 4)
SOURCEID = random.randint(1, 100)

class SampleTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            os.getenv('FLASK_CONFIG') or 'default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()


    def test_tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def get_api_headers(self, iftoken):
        if iftoken is True:
            return {
                'token': TOKEN,
                'Accept': 'application/json',
                'Content-Type': 'application/json'}
        else:
            return {
                'Accept': 'application/json',
                'Content-Type': 'application/json'}

    
    def test_d_app_exist(self):
        self.assertFalse(current_app is None)


    def test_a_management_auth(self):
        muxi = Team(name='test',count=3)
        superuser = User(
            name='cat',
            email='cat@test.com',
            tel='11111111111',
            role=7,
            team_id=1)
        muxi.creator = 1
        admin = User(
            name='dog',
            email='dog@test.com',
            tel='22222222222',
            role=1,
            team_id=1)
        usr = User(
            name='pig',
            email='pig@test.com',
            tel='33333333333',
            role=1,
            team_id=1)
        project = Project(name='test')
        rela = User2Project(user_id=1, project_id=1)
        db.session.add(muxi)
        db.session.add(superuser)
        db.session.add(admin)
        db.session.add(usr)
        db.session.add(project)
        db.session.add(rela)
        db.session.commit()
        response=self.client.post(
            url_for('api.login', _external=True),
            data=json.dumps({
                "username": 'cat',
            }),
            headers=self.get_api_headers(False))
        s = json.loads(response.data.decode('utf-8'))['token']
        global TOKEN
        TOKEN = s


# FEED PART

    def test_b_feed_new(self):
        response = self.client.post(
            url_for('api.newfeed', _external=True),
            data=json.dumps({
                "from":FROM[KIND-1],
                "action":FROM[KIND-1],
                "kind":KIND,
                "sourceID":SOURCEID}),
            headers=self.get_api_headers(True))
        self.assertTrue(response.status_code == 200)


    def test_c_feed_list(self):
        response = self.client.get(
            'http://localhost/api/v1.0/feed/list/',
            headers=self.get_api_headers(True))
        self.assertTrue(response.status_code == 200)

#END

