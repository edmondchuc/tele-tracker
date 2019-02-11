import logging
from flask import Flask
from config import Config
from controller import endpoints, routes
from flask_cors import CORS
from flask_login import LoginManager
from model.user import User


# Flask
app = Flask(__name__, template_folder=Config.TEMPLATES_DIR, static_folder=Config.STATIC_DIR)
app.register_blueprint(endpoints.endpoints)
app.register_blueprint(routes.routes)
app.secret_key = Config.FLASK_SECRET_KEY

# Flask-CORS
CORS(app) # CORS has been enabled for all domains

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'routes.login'
login_manager.login_message = None # Don't set any Flask flash messages


@login_manager.user_loader
def load_user(user_id):
    return User.get_user(user_id)


@app.before_first_request
def before_first_request():
    Config.init()


if __name__ == '__main__':
    logging.basicConfig(filename=Config.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    app.run(debug=Config.DEBUG, threaded=True)
