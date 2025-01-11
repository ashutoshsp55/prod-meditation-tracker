import os
import subprocess
from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Filepath for JSON storage
JSON_FILE = 'meditation_records.json'

# GitHub configuration (Token will be used from environment variable)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = f'https://ashutoshsp55:{GITHUB_TOKEN}@github.com/ashutoshsp55/prod-meditation-tracker.git'

# Helper function to load data from JSON file
def load_data():
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

# Helper function to save data to JSON file
def save_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to commit and push to GitHub
def push_to_github():
    try:
        # Configure Git user details (only once, if necessary)
        subprocess.run(['git', 'config', '--global', 'user.email', 'ashutoshraje3@gmail.com'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.name', 'ashutoshsp55'], check=True)

        remote_url = f'https://ashutoshsp55:{GITHUB_TOKEN}@github.com/ashutoshsp55/prod-meditation-tracker.git'

        # Check if origin exists, if not, add it
        remotes = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True, check=True).stdout
        if 'origin' not in remotes:
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
        else:
            subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)

        # Commit and push the changes
        subprocess.run(['git', 'add', 'meditation_records.json'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Updated meditation records'], check=True)
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error pushing to GitHub: {e}")

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

    # Push changes to GitHub
    push_to_github()

    return jsonify({"message": "Record added and pushed to GitHub successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
