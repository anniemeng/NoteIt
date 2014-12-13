import os

from flask.ext.script import Manager, Shell
from app import create_app, db
from app.models import User, Document
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Document=Document)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def populate():
  db.drop_all()
  db.create_all()

  annie = User(name="Annie Meng", email="anniezmeng@gmail.com", password="password")
  remi = User(name="Irem Oz", email="ioz@gmail.com", password="password")
  db.session.add(annie)
  db.session.add(remi)

if __name__ == '__main__':
    manager.run()