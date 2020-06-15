from flask import Flask, render_template
from flask import request, make_response
from flask_bootstrap import Bootstrap


app = Flask(__name__) 
Bootstrap(app)


@app.route('/')
def index():
    response = make_response('<h1>This doc carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    user_agent = request.headers.get('User-Agent')
    # return '<h1>Your browser is %s!</h1>' % user_agent
    return response

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
