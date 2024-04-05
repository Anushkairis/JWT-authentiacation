from flask import Flask
from authController import app as auth_app

# A Flask application instance
app = Flask(__name__)

# Registering the authController Blueprint with the main application
app.register_blueprint(auth_app)


# Route for the home page
@app.route("/")
def home():
    return "Hello, this is the home page!"


# Run
if __name__ == '__main__':
    # Enable debugging mode for development
    app.run(debug=True,host='0.0.0.0', port=5000)
