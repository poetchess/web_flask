from flask import Flask

'''
A Flask application must create an application instance.
Web server passes all requests it receives from clients to this object for 
handling, using WSGI protocol.
'''
app = Flask(__name__)

#The association b/w a URL and the function that handles it is called a route.
#Functions like 'index()' are called view functions.
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)