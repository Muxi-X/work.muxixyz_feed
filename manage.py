import os
import pika
from flask_script import Manager, Shell#, Command
from flask_migrate import Migrate, MigrateCommand
from work_muxixyz_app import create_app, db
from sqlalchemy import func
from work_muxixyz_app.models import Feed, Team, Group, User, Project, Message, Statu, File, Comment

#export PYTHONIOENCODING="UTF-8"

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
MQHOST = os.getenv("MQHOST") or "localhost"
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def receive():
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=MQHOST))
    channel = connection.channel()
    feed_queue = channel.queue_declare(queue='feed')
    def callback(ch, method, properties, body):
        feed = eval(body.decode())
        lastestid = db.session.query(func.max(Feed.id))
        last_feed = Feed.query.filter_by(id=lastestid).first()
        if last_feed == None:
            feed['divider'] = True
        elif last_feed.kind == feed['kind']:
            feed['divider'] = False
        else:
            feed['divider'] = True
        feed = Feed(
            time=feed['time'],
            avatar_url=feed['avatar_url'],
            user_id=feed['uid'],
            action=feed['action'],
            kind=feed['kind'],
            sourceid=feed['source'],
            divider=feed['divider'])
        db.session.add(feed)
        db.session.commit()
    channel.basic_consume(
        callback,
        queue='feed',
        no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    manager.run()
    app.run(debug=True)
