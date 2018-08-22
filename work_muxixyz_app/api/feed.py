import pika
import os
import requests
from flask import jsonify, request, current_app, url_for, Flask
from . import api
from .. import db
from ..models import Team, Group, User, User2Project, Message, Statu, File, Comment, Project
from ..decorator import login_required
from work_muxixyz_app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

num = 0
feed_stream = []

@api.route('/feed/new/', methods=['POST'])
@login_required
def newfeed(uid):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()
    FROM = str(request.get_json().get('from').decode('utf-8'))
    KIND = str(request.get_json().get('kind'))
    ACTION = str(request.get_json().get('action').decode('utf-8'))
    SOURCEID = str(request.get_json().get('sourceID'))
    a_feed = FROM + '/' + KIND + '/' + ACTION + '/' + SOURCEID
    print a_feed
    maxid = db.session.query(func.max(User.id)).one()
    for xid in range(1, maxid[0]+1): 
        channel.queue_declare(
            queue=str(xid))
        channel.basic_publish(
            exchange='',
            routing_key=str(xid),
            body=str(a_feed),
            properties=pika.BasicProperties(
                delivery_mode=2))
    connection.close()
    response = jsonify({"message":"feed add successfully"})
    response.status_code = 200
    return response


@api.route('/feed/list/', methods=['GET'])
@login_required
def getfeedlist(uid):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()
    feed_queue = channel.queue_declare(queue=str(uid))
    def callback(ch, method, properties, body):
        global feed_stream, num
        feed = body
        feed = feed.split("/", 3)
        feed_stream.append(feed)
        num += 1
        if (feed_queue.method.message_count - num) == 0:
            print feed_stream
            channel.stop_consuming()
    channel.basic_consume(
        callback,
        queue=str(uid),
        no_ack=True)
    channel.start_consuming()
    response = jsonify({
        "feed_stream": feed_stream})
    response.status_code = 200
    return response 
