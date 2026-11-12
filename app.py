
import os

from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv

from extensions import db, login_manager, csrf  

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
db.init_app(app)
csrf.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "admin_auth.admin_login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"

from database.models import Event, DeletedEvent, Admin


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Admin, int(user_id))
    except (ValueError, TypeError):
        return None


migrate = Migrate(app, db)

from routes.event_routes import event_bp
from routes.admin_auth_routes import admin_auth_bp
from routes.admin_approval_routes import admin_approval_bp
from routes.admin_notification_routes import admin_notification_bp

app.register_blueprint(event_bp)
app.register_blueprint(admin_auth_bp)
app.register_blueprint(admin_approval_bp)
app.register_blueprint(admin_notification_bp)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
