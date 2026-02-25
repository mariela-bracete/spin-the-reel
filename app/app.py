from flask import Flask, render_template, request
from routes import routes  # Import the Blueprint

app = Flask(__name__)

app.register_blueprint(routes)  # Register the Blueprint

if __name__ == '__main__':
    app.run(debug=True)

