import pika
import os
import time
import requests
from flask import jsonify, request, current_app, url_for, Flask
from . import api
from .. import db
from ..models import Feed, Team, Group, User, User2Project, Message, Statu, File, Comment, Project
from ..decorator import login_required
from work_muxixyz_app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from ..mq import newfeed


#KIND = ['Statu', 'Project', 'Doc', 'Comment', 'Team', 'User', 'File']
MQHOST = os.getenv("MQHOST") or "localhost"
num = 0
feed_d = {}
feed_stream = []
divider_name = ''
pid = 0

#权限判定函数
def ifProject(sid): 
    if sid  not in pidlist:
        continue
    else:
        global divider_name, pid
        divider_name = Project.query.filter_by(id=feed.sourceid).first().name
        pid = sid

def ifDocFile(sid):
    global pid, divider_name
    pid = File.query.filter_by(id=sid).first().project_id
    if pid not in pidlist:
        continue
    else:
        divider_name = Project.query.filter_by(id=pid).first().name

def ifComment(sid):
    global pid, divider_name
    comment = Comment.query.filter_by(id=sid).first()
    if comment.kind == 1:
        file1 = File.query.filter_by(id=comment.fileID).first()
        if file1.project_id not in pidlist:
            continue
        else:
            divider_name = Project.query.filter_by(id=file1.project_id).first().name
            pid = file1.project_id
    else:
        pid = 0
        divider_name = 'status'

def ifTeam(sid):
    global pid, divider_name
    pid = Project.query.filter_by(team_id=sid).first()
    if pid not in pidlist:
        continue
    divider_name = Project.query.filter_by(id=pid).first().name


@api.route('/feed/list/<int:page>/', methods=['GET'], endpoint="getfeedlist")
@login_required(1)
def getfeedlist(uid,page):
    feeds = Feed.query.all()
    pidlist = User2Project.query.filter_by(user_id=uid).all()
    for feed in feeds:
        global num
        num += 1        
        if feed.kind == 1:
            ifProject(feed.sourceid)
        if feed.kind == 2 or feed.kind == 6:
            ifDocFile(feed.sourceid)
        if feed.kind == 3:
            ifComment(feed.sourceid)
        if feed.kind == 4:
            ifTeam(feed.sourceid)
        feed_time = feed.time.split(" ",2)
        feed_d['time_d']=feed_time[0]
        feed_d['time_s']=feed_time[1]
        feed_d['avatar_url']=feed.avatar_url
        feed_d['uid']=feed.user_id
        feed_d['action']=feed.action
        feed_d['kind']=feed.kind
        feed_d['sourceID']=feed.sourceid
        feed_d['divider']=feed.divider
        if feed.kind == 0:
            feed_d['divider_id'] = 0
            feed_d['divider_name'] = 'status'
        else:
            feed_d['divider_id'] = pid
            feed_d['divider_id'] = divider_name
        feed_c = feed_d.copy()
        if num <= 40 * page and num > 40 * (page-1):
            feed_stream.append(feed_c)
        elif num > 40 * page:
            break
    response = jsonify({
        "feed_stream": feed_stream,
        "page": page})
    response.status_code = 200
    return response 
