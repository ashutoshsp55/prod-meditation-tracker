from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Filepath for JSON storage
JSON_FILE = 'meditation_records.json'

# Helper function to load data from JSON file
def load_data():
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

# Helper function to save data to JSON file
def save_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Route: Main Page
@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', total_time=data['total_time'], records=data['records'])

# Route: Add Meditation Record
@app.route('/add', methods=['POST'])
def add_record():
    # Load existing data
    data = load_data()
    
    # Get input from form
    meditation_time = int(request.form['meditation_time'])
    date_added = datetime.now().strftime('%Y-%m-%d')
    
    # Update data
    data['total_time'] += meditation_time
    data['records'].append({'time': meditation_time, 'date': date_added})
    
    # Save updated data
    save_data(data)
    
    return jsonify({"message": "Record added successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

