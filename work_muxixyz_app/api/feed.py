# -*- coding: utf-8 -*-
import pika
import os
import time
import requests
from flask import jsonify, request, current_app, url_for, Flask
from . import api
from .. import db
from ..models import Feed, Team, Group, User, User2Project, Message, Statu, File, Comment, Project, Doc
from ..decorator import login_required
from work_muxixyz_app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from ..mq import newfeed


#KIND = ['Statu', 'Project', 'Doc', 'Comment', 'Team', 'User', 'File']
MQHOST = os.getenv("WORKBENCH_MQHOST") or "localhost"
num = 0
feed_d = {}
divider_name = ''
pid = 0


#权限判定函数
def cutdown(action):
    action = action.split(" ",2)[1]
    if action[:2] == "删除":
        return 1;

def ifProject(sid, action): 
    cutdown(action)
    global pidlist
    if sid  not in pidlist:
        return 1;
    else:
        global divider_name, pid
        divider_name = Project.query.filter_by(id=feed.sourceid).first().name
        pid = sid
        return 0;

def ifDoc(sid, action):
    cutdown(action)
    global pid, divider_name, pidlist
    pid = Doc.query.filter_by(id=sid).first().project_id
    if pid not in pidlist:
        return 1;
    else:
        divider_name = Project.query.filter_by(id=pid).first().name
        return 0;

def ifFile(sid, action):
    cutdown(action)
    global pid, divider_name, pidlist
    pid = File.query.filter_by(id=sid).first().project_id
    if pid not in pidlist:
        return 1;
    else:
        divider_name = Project.query.filter_by(id=pid).first().name
        return 0;

def ifComment(sid, action):
    cutdown(action)
    global pid, divider_name, pidlist
    comment = Comment.query.filter_by(id=sid).first()
    if comment.kind == 1:
        doc = Doc.query.filter_by(id=comment.doc_id).first()
        if doc.project_id not in pidlist:
            return 1;
        else:
            divider_name = Project.query.filter_by(id=doc.project_id).first().name
            pid = file1.project_id
            return 0;
    else:
        pid = 0
        divider_name = 'status'
        return 0;

def ifTeam(sid, action):
    cutdown(action)
    global pid, divider_name, pidlist
    pid = Project.query.filter_by(team_id=sid).first()
    if pid not in pidlist:
        return 1;
    divider_name = Project.query.filter_by(id=pid).first().name
    return 0;

@api.route('/feed/list/<int:page>/', methods=['GET'], endpoint="getfeedlist")
@login_required(1)
def getfeedlist(uid,page):
    global pidlist, num
    pidlist = []
    feed_stream = []
    num = 0
    feeds = Feed.query.allnumcount = Feed.query.count()
    pidlist = User2Project.query.filter_by(user_id=uid).all()
    for feed in feeds:
        #global num
        num += 1        
        if feed.kind == 1:
            if ifProject(feed.sourceid, feed.action) == 1:
                continue
        if feed.kind == 2:
            if ifDoc(feed.sourceid, feed.action) == 1:
                continue
        if feed.kind == 3:
            if ifComment(feed.sourceid, feed.action) == 1:
                continue
        if feed.kind == 4:
            if ifTeam(feed.sourceid, feed.action) == 1:
                continue
        if feed.kind == 6:
            if ifFile(feed.sourceid, feed.action) == 1:
                continue
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
        #elif num > 40 * page:
        #    break
    response = jsonify({
        "feed_stream": feed_stream,
        "page": page,
        "count": num})
    response.status_code = 200
    return response 


@api.route('/feed/list/personal/<int:page>/', methods=['GET'], endpoint="getuserfeedlist")
@login_required(1)
def getuserfeedlist(uid,page):
    global num
    pidlist = []
    num = 0
    feed_stream = []
    feeds = Feed.query.all()
    #count = Feed.query.count()
    pidlist = User2Project.query.filter_by(user_id=uid).all()
    for feed in feeds:
        #global num
        num += 1        
        if feed.user_id != uid:
            continue
        if feed.kind == 1:
            ifProject(feed.sourceid, feed.action)
        if feed.kind == 2 or feed.kind == 6:
            ifDocFile(feed.sourceid, feed.action)
        if feed.kind == 3:
            ifComment(feed.sourceid, feed.action)
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
            feed_d['divider_id'] = 1
            feed_d['divider_name'] = 'status'
        else:
            feed_d['divider_id'] = pid
            feed_d['divider_id'] = divider_name
        feed_c = feed_d.copy()
        if num <= 40 * page and num > 40 * (page-1):
            feed_stream.append(feed_c)
        #elif num > 40 * page:
        #    break
    response = jsonify({
        "feed_stream": feed_stream,
        "page": page,
        "count": num})
    response.status_code = 200
    return response 

