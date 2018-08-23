'''coding = utf-8'''
import unittest
import os
import random
import json
from flask import current_app, url_for#, jsonify, Flask
from work_muxixyz_app import create_app, db
from work_muxixyz_app.models import Feed, Team, User, Group, Project, Message, Statu, File, Comment, User2Project

#db = SQLAlchemy()
FROM = ['status', 'project', 'doc','team', 'comments', 'teams', 'user', 'file']
KIND = random.randint(0, 6)
SOURCEID = 1#random.randint(1, 100)

class SampleTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            os.getenv('FLASK_CONFIG') or 'default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()


    def test_teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def get_api_headers(self, iftoken):
        if iftoken is True:
            return {
                'token': TOKEN,
                'Accept': 'application/json',
                'Content-Type': 'application/json'}
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'}

 
    def test_d_app_exist(self):
        self.assertFalse(current_app is None)


    def test_a_management_auth(self):
        muxi = Team(name='test', count=3)
        muxi.creator = 1
        db.session.add(muxi)
        db.session.commit()
        superuser = User(
            name='cat',
            email='cat@test.com',
            tel='11111111111',
            role=7,
            team_id=1)
        db.session.add(superuser)
        db.session.commit()
        admin = User(
            name='dog',
            email='dog@test.com',
            tel='22222222222',
            role=1,
            team_id=1)
        db.session.add(admin)
        db.session.commit()
        usr = User(
            name='pig',
            email='pig@test.com',
            tel='33333333333',
            role=1,
            team_id=1)
        db.session.add(usr)
        db.session.commit()
        project = Project(name='test')
        db.session.add(project)
        db.session.commit()
        rela = User2Project(user_id=1, project_id=1)
        db.session.add(rela)
        db.session.commit()
        file1 = File(url='test',project_id=1)
        db.session.add(file1)
        db.session.commit()
        statu = Statu(content='test', user_id=1)
        db.session.add(statu)
        db.session.commit()
        comment = Comment(content='test',kind=1,file_id=1)
        db.session.add(comment)
        db.session.commit()
        response = self.client.post(
            url_for('api.login', _external=True),
            data=json.dumps({
                "username": 'cat'}),
            headers=self.get_api_headers(False))
        result_t = json.loads(response.data.decode('utf-8'))['token']
        global TOKEN
        TOKEN = result_t


# FEED PART

    def test_b_feed_new(self):
        response = self.client.post(
            url_for('api.nf', _external=True),
            data=json.dumps({
                "avatar_url":'www.baidu.com',
                "action":FROM[KIND],
                "kind":KIND,
                "sourceID":SOURCEID}),
            headers=self.get_api_headers(True))
        self.assertTrue(response.status_code == 200)


    def test_c_feed_list(self):
        response = self.client.get(
            'http://localhost/api/v1.0/feed/list/1/',
            headers=self.get_api_headers(True))
        self.assertTrue(response.status_code == 200)
        print(response.data)
#END
