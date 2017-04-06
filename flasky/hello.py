import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

'''
A Flask application must create an application instance.
Web server passes all requests it receives from clients to this object for 
handling, using WSGI protocol.
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string, really?'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    '''
        The users attribute added to model Role represents the object-oriented 
        view of the relationship. Given an instance of class Role, the users 
        attribute will return the list of users associated with that role. The 
        first argument to db.relationship() indicates what model is on the 
        other side of the relationship. This model can be provided as a string 
        if the class is not yet defined.

        The backref argument to db.relationship() defines the reverse direction
        of the relationship by adding a role attribute to the User model. This 
        attribute can be used instead of role_id to access the Role model as an
        object instead of as a foreign key.
    '''
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username

'''
    Having to import the database instance and the models each time a shell 
    session is started is tedious work. To avoid having to constantly repeat 
    these imports, the Flask-Script's shell command can be configured to 
    automatically import certain objects.
'''
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

#The association b/w a URL and the function that handles it is called a route.
#Functions like 'index()' are called view functions.

#'methods' argument allows Flask to register the view function as a handler
#for GET and POST requests.
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    #Browsers repeat the last request  they have sent when they are asked to 
    #refresh the page. When the last request sent is a POST request with form
    #data, a refresh would cause a duplicate form submission, which in almost
    #all cases is not the desired action.

    #Using Post/Redirect/Get pattern

    #validate_on_submit() returns True if the form was submitted and the data 
    #has been accepted by all the field validators.
    if form.validate_on_submit():

        #Application can remember things from one request to the next by 
        #storing them in the user session, private storage that is available to
        #each connected client. The user session is one of the variables 
        #associated with the request context and is called 'session'.
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        #Generate the HTTP redirect response. Obtaining the redirected URL 
        #using url_for() is encourged.
        return redirect(url_for('index'))

    #using get() to request a dictionary key avoids an exception for keys that 
    #aren't found, it will return a default value of None for a missing key.
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

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
    #db.create_all()
    manager.run()
