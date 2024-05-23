from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure Flask to connect to the cloudapp database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/cloudapp.db'  # Replace with your actual database URI
db = SQLAlchemy(app)

# Define a model for the resource table
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image_url = db.Column(db.String(100))

# Route to load data
@app.route('/')
def index():
    # Query the database to retrieve the first 10 resources
    resources = Resource.query.limit(10).all()
    return render_template('properties2.html', resources=resources)

if __name__ == '__main__':
    app.run(debug=True)
