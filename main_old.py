from flask import Flask, request, render_template, redirect, url_for, jsonify
import json
import os
import nltk
import uuid

# Download NLTK data quietly (runs once, kept for potential future use)
nltk.download('punkt', quiet=True)

# Initialize Flask app
app = Flask(__name__)
DATA_FILE = 'flashcards_data.json'

# Load all data (folders and flashcards)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
    return {'folders': [], 'uncategorized': []}

# Save all data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Migrate old flashcards.json to new structure if needed
def migrate_old_data():
    if os.path.exists('flashcards.json') and not os.path.exists(DATA_FILE):
        with open('flashcards.json', 'r') as f:
            content = f.read().strip()
            if content:
                old_flashcards = json.loads(content)
                new_data = {'folders': [], 'uncategorized': old_flashcards}
                save_data(new_data)
                return new_data
    return load_data()

# Get all flashcards (for review - combines all folders)
def get_all_flashcards():
    data = load_data()
    all_cards = data['uncategorized'].copy()
    for folder in data['folders']:
        all_cards.extend(folder['flashcards'])
    return all_cards

# Route for the main page (add flashcards)
@app.route('/', methods=['GET', 'POST'])
def index():
    data = migrate_old_data()
    if request.method == 'POST':
        word_list = request.form['words'].split('\n')
        for line in word_list:
            if ':' in line:
                word, meaning = line.split(':', 1)
                data['uncategorized'].append({'word': word.strip(), 'meaning': meaning.strip()})
        save_data(data)
    return render_template('input.html')

# Route for the review page (flip cards with swipe)
@app.route('/review')
def review():
    flashcards = get_all_flashcards()
    current_index = 0
    return render_template('review.html', flashcards=flashcards, current_index=current_index)

# Route for the my flashcards page (list all flashcards and folders)
@app.route('/my-flashcards')
def my_flashcards():
    data = load_data()
    return render_template('my-flashcards.html', folders=data['folders'], uncategorized=data['uncategorized'])

# Route to create a new folder
@app.route('/create-folder', methods=['POST'])
def create_folder():
    data = load_data()
    folder_name = request.form.get('folder_name', '').strip()
    if folder_name:
        new_folder = {
            'id': str(uuid.uuid4()),
            'name': folder_name,
            'flashcards': []
        }
        data['folders'].append(new_folder)
        save_data(data)
    return redirect(url_for('my_flashcards'))

# Route to move flashcard to folder
@app.route('/move-flashcard', methods=['POST'])
def move_flashcard():
    data = load_data()
    flashcard_index = int(request.form.get('flashcard_index', 0))
    from_folder = request.form.get('from_folder', '')
    to_folder = request.form.get('to_folder', '')
    
    # Find and remove the flashcard from its current location
    flashcard = None
    if from_folder == 'uncategorized':
        flashcard = data['uncategorized'].pop(flashcard_index)
    else:
        for folder in data['folders']:
            if folder['id'] == from_folder:
                flashcard = folder['flashcards'].pop(flashcard_index)
                break
    
    # Add flashcard to new location
    if flashcard:
        if to_folder == 'uncategorized':
            data['uncategorized'].append(flashcard)
        else:
            for folder in data['folders']:
                if folder['id'] == to_folder:
                    folder['flashcards'].append(flashcard)
                    break
    
    save_data(data)
    return redirect(url_for('my_flashcards'))

# Route to delete a folder
@app.route('/delete-folder/<folder_id>', methods=['POST'])
def delete_folder(folder_id):
    data = load_data()
    for i, folder in enumerate(data['folders']):
        if folder['id'] == folder_id:
            # Move flashcards back to uncategorized
            data['uncategorized'].extend(folder['flashcards'])
            data['folders'].pop(i)
            break
    save_data(data)
    return redirect(url_for('my_flashcards'))

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)