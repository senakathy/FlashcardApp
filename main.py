from flask import Flask, request, render_template
import json
import os

app = Flask(__name__)
FLASHCARDS_FILE = 'flashcards.json'

def load_flashcards():
    if os.path.exists(FLASHCARDS_FILE):
        with open(FLASHCARDS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_flashcards(flashcards):
    with open(FLASHCARDS_FILE, 'w') as f:
        json.dump(flashcards, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    flashcards = load_flashcards()
    if request.method == 'POST':
        word_list = request.form['words'].split('\n')
        for line in word_list:
            if ':' in line:
                word, meaning = line.split(':', 1)
                flashcards.append({'word': word.strip(), 'meaning': meaning.strip(), 'folder': ''})
        save_flashcards(flashcards)
    return render_template('input.html', flashcards=flashcards)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)