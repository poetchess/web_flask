from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
'''
A Flask application must create an application instance.
Web server passes all requests it receives from clients to this object for 
handling, using WSGI protocol.
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string, really?'

manager = Manager(app)
bootstrap = Bootstrap(app)

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
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        #Generate the HTTP redirect response. Obtaining the redirected URL 
        #using url_for() is encourged.
        return redirect(url_for('index'))

    #using get() to request a dictionary key avoids an exception for keys that 
    #aren't found, it will return a default value of None for a missing key.
    return render_template('index.html', form=form, name=session.get('name'))

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
