from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
'''
A Flask application must create an application instance.
Web server passes all requests it receives from clients to this object for 
handling, using WSGI protocol.
'''
app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

#The association b/w a URL and the function that handles it is called a route.
#Functions like 'index()' are called view functions.
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

#The portion enclosed in angle brackets is the dynamic part.
#Dynamic components in routes are strings by default.
#When the view function is invoked, Flask sends the dynamic component as an
#argument.
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
