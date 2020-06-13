from flask import Flask, render_template
from flask import request, make_response
# from flask.ext.script import Manager

app = Flask(__name__)
# manager = Manager(app)


@app.route('/')
def index():
    response = make_response('<h1>This doc carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    user_agent = request.headers.get('User-Agent')
    # return '<h1>Your browser is %s!</h1>' % user_agent
    return response

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', val=name)


if __name__ == "__main__":
    app.run(debug=True)
    # manager.run()