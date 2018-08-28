from flask import (Flask, g, jsonify, render_template, flash, redirect,
                    url_for)
from flask.ext.login import LoginManager

from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr

from auth import auth

import config
import forms
import models

from resources.todos import todos_api
from resources.users import users_api


app = Flask(__name__)
"""
app.secret_key = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.register_blueprint(todos_api)
app.register_blueprint(users_api, url_prefix='/api/v1')
"""

limiter = Limiter(app, global_limits=[config.DEFAULT_RATE], key_func=get_ipaddr)
limiter.limit("40/day")(users_api)
limiter.limit(config.DEFAULT_RATE, per_method=True,
                methods=["post", "put", "delete"])(todos_api)
#limiter.exempt(todos_api)

"""
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    Connect to the database before each request.
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    Close the database connection after each request.
    g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registerd!", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            pasword=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
"""

@app.route('/')
def my_todos():
    todos = models.Todo.select()
    return render_template('index.html', todos=todos)


@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})



if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
