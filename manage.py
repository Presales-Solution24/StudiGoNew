# manage.py
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.models import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

# Add db commands to manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
