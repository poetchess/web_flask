from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap

'''
A Flask application must create an application instance.
Web server passes all requests it receives from clients to this object for 
handling, using WSGI protocol.
'''
app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)

#The association b/w a URL and the function that handles it is called a route.
#Functions like 'index()' are called view functions.
@app.route('/')
def index():
    return render_template('index.html')

#The portion enclosed in angle brackets is the dynamic part.
#Dynamic components in routes are strings by default.
#When the view function is invoked, Flask sends the dynamic component as an
#argument.
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    manager.run()
