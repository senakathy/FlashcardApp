from flask import Flask, request, render_template
import json
import os
import nltk

# Download NLTK data quietly (runs once, kept for potential future use)
nltk.download('punkt', quiet=True)

# Initialize Flask app
app = Flask(__name__)
FLASHCARDS_FILE = 'flashcards.json'

# Load flashcards from the JSON file
def load_flashcards():
    if os.path.exists(FLASHCARDS_FILE):
        with open(FLASHCARDS_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                return json.loads(content)
            else:
                return []
    return []

# Save flashcards to the JSON file
def save_flashcards(flashcards):
    with open(FLASHCARDS_FILE, 'w') as f:
        json.dump(flashcards, f)

# Route for the main page (add flashcards)
@app.route('/', methods=['GET', 'POST'])
def index():
    flashcards = load_flashcards()
    if request.method == 'POST':
        word_list = request.form['words'].split('\n')
        for line in word_list:
            if ':' in line:
                word, meaning = line.split(':', 1)
                flashcards.append({'word': word.strip(), 'meaning': meaning.strip()})
        save_flashcards(flashcards)
    return render_template('input.html', flashcards=flashcards)

# Route for the review page (flip cards with swipe)
@app.route('/review')
def review():
    flashcards = load_flashcards()
    current_index = 0  # Start with the first card
    return render_template('review.html', flashcards=flashcards, current_index=current_index)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)