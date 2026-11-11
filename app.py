
import os

from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv

from extensions import db

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)

# Application configuration
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database with Flask
db.init_app(app)

# Initialize migrations
migrate = Migrate(app, db)

# Import database models
from database.models import Event

# Import and register event routes
from routes.event_routes import event_bp

app.register_blueprint(event_bp)


# Homepage
@app.route("/")
def home():
    return render_template("index.html")


# Run application
if __name__ == "__main__":
    app.run(debug=True)
