from flask_script import Manager
from test_col_diamon import app
manager=Manager(app)

@manager.command
def hello():
    'print hello jj string'
    print "hello jj"

if __name__ == "__main__":
    manager.run()
