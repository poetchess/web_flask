from flask import Flask, render_template
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
    name = None
    form = NameForm()

    #validate_on_submit() returns True if the form was submitted and the data 
    #has been accepted by all the field validators.
    if form.validate_on_submit():
        name = form.name.data
        #clear the form data. Otherwise, it will be rendered on the page.
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

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
