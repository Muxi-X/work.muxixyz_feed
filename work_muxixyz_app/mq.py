import pika
import time
import datetime
import os
from work_muxixyz_app import db
from work_muxixyz_app.models import User

MQHOST = os.getenv("WORKBENCH_MQHOST")
MQUSERNAME = os.getenv("WORKBENCH_MQUSERNAME")
MQPASSWORD = os.getenv("WORKBENCH_MQPASSWORD")
MQQUEUENAME = "feed"

class MessageQueue:
    def __init__(self):
        self.host = MQHOST
        self.username = MQUSERNAME 
        self.password = MQPASSWORD
        self.queuename = MQQUEUENAME

    def __enter__(self):
        """
        connection and declear
        """
        pass

    def __exit__(self):
        """
        close
        """
        pass

    def publish(self, body):
        pass


def newfeed2(uid, action, source_kind_id, source_object_id, source_project_id=-1):
    """
    uid: user id
    action: string in [["加入", "创建", "编辑", "删除", "评论", "移动"]]
    source_kind_id: source_list = ["", "团队", "项目", "文档", "文件", "文件夹", "进度"]
    source_object_id: 资源在数据库中的id
    source_project_id: file or doc 所在项目的id

    ***** a feed's structure *****
    {
        "user": {
            "name": string,
            "id": integer,
            "avatar_url": string
        },
        "action": string,
        "source": {
            "kind_id": integer,
            "object_id": integer,
            "project_id": integer // 没有为-1 
        },
        "time": "2018-10-21-23:15:56" // yyyy-mm-dd-HH:MM:SS  datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S') 
        /* 在返回时扫描&添加
        "split": {
            "ifsplit": boolean,
            "kind_id": integer // 显示的kind_id
        }
        */
    }
    
    """
    user = User.query.filter_by(id=uid).first() or None
    time = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S') 
    a_feed = {
        "user": {
            "name": user.name,
            "id": user.id,
            "avatar_url": user.avatar
        },
        "action": action,
        "source": {
            "kind_id": source_kind_id,
            "object_id": source_object_id,
            "project_id": source_project_id
        },
        "time": time
    }

    if not check_feed(a_feed):
        raise FeedException
    
    with MessageQueue() as q:
        q.publish(a_feed)


def check_feed(feed_to_be_checked):
    """
    return: true if ok, false if failed
    """
    pass


class FeedException(Exception):
    pass



"""

def newfeed(uid, action, kind, sourceID):
    credentials = pika.PlainCredentials(MQUSERNAME, MQPASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=MQHOST,
            port=5672,
            virtual_host='/',
            credentials=credentials))
    channel = connection.channel()
    time1 = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    user = User.query.filter_by(id=uid).first()
    username = user.name
    avatar_url = user.avatar
    if action is not "加入":
        print("username:" + username)
        print("action:" + action)
        ACTION = username + ' ' + action + "了："
    else:
        ACTION = username + ' ' + action
    KIND = kind
    SOURCEID = sourceID
    a_feed = {
        'time':time1,
        'avatar_url':avatar_url,
        'uid':uid,
        'action':ACTION,
        'kind':KIND,
        'sourceid':SOURCEID}
    channel.queue_declare(queue='feed')
    channel.basic_publish(
        exchange='',
        routing_key='feed',
        body=str(a_feed),
        properties=pika.BasicProperties(
            delivery_mode=2))
    connection.close()

"""
