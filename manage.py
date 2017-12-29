#!/usr/bin/env python
import os
from todoist import create_app, db
from todoist.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

todoist = create_app('default')
manager = Manager(todoist)
migrate = Migrate(todoist, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
