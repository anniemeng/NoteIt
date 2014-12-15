import os

from flask.ext.script import Manager, Shell, Server
from app import create_app, db
from app.models import User, Document, Note
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Document=Document, Note=Note)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def populate():
    db.drop_all()
    db.create_all()

    annie = User(name="Annie Meng", email="anniezmeng@gmail.com",
                 password="password")
    lili = User(name="Lili Dworkin", email="lili@gmail.com",
                password="password")
    db.session.add(annie)
    db.session.add(lili)


@manager.command
def customServer(host, port):
    app.run(host=host, port=int(port))

if __name__ == '__main__':
    manager.run()
