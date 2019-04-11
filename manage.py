import os
import pika
from flask_script import Manager, Shell#, Command
from flask_migrate import Migrate, MigrateCommand
from work_muxixyz_app import create_app, db
from sqlalchemy import func
from work_muxixyz_app.models import Feed, Team, Group, User, Project, Message, Statu, File, Comment
import pymysql

#export PYTHONIOENCODING="UTF-8"

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
MQHOST = os.getenv("WORKBENCH_MQHOST") or "localhost"
MQPORT = os.getenv("WORKBENCH_MQPORT") or "5672"
MQPORT = int(MQPORT)
MQUSERNAME = os.getenv("WORKBENCH_MQUSERNAME") 
MQPASSWORD = os.getenv("WORKBENCH_MQPASSWORD") 
manager.add_command('db', MigrateCommand)


DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = os.getenv("WORKBENCH_USERNAME")
PASSWORD = os.getenv("WORKBENCH_PASSWORD")
HOST = os.getenv("WORKBENCH_HOST")
PORT = 3306
DATABASE = os.getenv("WORKBENCH_DBNAME")



def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

#@manager.command
#def test_status():
#    import unittest
#    tests = unittest.TestLoader().discover('test_status')
#    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def test_feed():
    import unittest
    tests = unittest.TestLoader().discover('test_feed')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def receive(): 
    credentials = pika.PlainCredentials(MQUSERNAME, MQPASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=MQHOST,
            port=MQPORT,
            virtual_host='/',
            credentials=credentials))
    channel = connection.channel()
    feed_queue = channel.queue_declare(queue='feed')
    
    def callback(ch, method, properties, body):
        feed = eval(body.decode())
        print("received:")
        print(feed)
        print()
        try:
            feedinsert = Feed(
                    userid = feed.get("user").get("id"),
                    username = feed.get("user").get("name"),
                    useravatar = feed.get("user").get("avatar_url"),
                    action = feed.get("action"),
                    source_kindid = feed.get("source").get("kind_id"),
                    source_objectid = feed.get("source").get("object_id"),
                    source_projectid = feed.get("source").get("project_id"),
                    source_objectname = feed.get("source").get("object_name"),
                    source_projectname = feed.get("source").get("project_name"),
                    timeday = feed.get("timeday"),
                    timehm = feed.get("timehm")
                )
        except:
            pass
        db.session.add(feedinsert)
        db.session.commit()
        
        checkfullandremove()


    channel.basic_consume(
        callback,
        queue='feed',
        no_ack=True)

    print("Starting receive message...")

    channel.start_consuming()

def checkfullandremove():
    FULL=10000
    PRE=1000
    try:
        feedcount = Feed.query.count()
        print("feedcount:" + str(feedcount))
        # 删除前1000条
        if feedcount > FULL:
            db = pymysql.connect(host=HOST, port=3306, user=USERNAME, passwd=PASSWORD, db=DATABASE)
            cursor = db.cursor()
            sql = "delete from feeds order by id asc limit " + str(PRE) + ";"
            effect_rows = cursor.execute(sql)
            print(str(effect_rows) + " rows deleted")
            db.commit()
            cursor.close()
            db.close()
    except Exception as e:
        print("exception:" + str(e))
        db.rollback()



if __name__ == '__main__':
    manager.run()
    app.run(debug=True)
