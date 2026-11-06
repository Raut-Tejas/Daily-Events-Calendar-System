
from flask import Flask

# Create the Flask application
app = Flask(__name__)


# Home page route
@app.route("/")
def home():
    return """
    <h1>Daily Events & Indian Calendar</h1>
    <p>Welcome to our application!</p>
    <p>Discover Indian festivals, holidays, and daily events.</p>
    """


# Run the application
if __name__ == "__main__":
    app.run(debug=True)
