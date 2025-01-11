from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Setup the database URI for PostgreSQL on Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://meditation_data_user:5FJ0KiAlztLHXIOVxu8ZDxXHQUDKVLxn@dpg-cu1bl9hu0jms738hr6dg-a/meditation_data')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary overhead

db = SQLAlchemy(app)

# Define the MeditationRecord model
class MeditationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meditation_time = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Record({self.meditation_time}, '{self.date_added}')"

# Route: Main Page
@app.route('/')
def index():
    records = MeditationRecord.query.all()
    total_time = sum(record.meditation_time for record in records)
    return render_template('index.html', total_time=total_time, records=records)

# Route: Add Meditation Record
@app.route('/add', methods=['POST'])
def add_record():
    meditation_time = int(request.form['meditation_time'])
    date_added = datetime.now().strftime('%Y-%m-%d')

    # Create a new record in the database
    new_record = MeditationRecord(meditation_time=meditation_time, date_added=date_added)
    db.session.add(new_record)
    db.session.commit()

    return jsonify({"message": "Record added successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
