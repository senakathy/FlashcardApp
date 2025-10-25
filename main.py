from flask import Flask, request, render_template 
import json
import os
import nltk
from googletrans import Translator  # For translating meanings
nltk.download('punkt', quiet=True)

app = Flask(__name__)
FLASHCARDS_FILE = 'flashcards.json'

def load_translation_cache():
    cache_file = 'translation_cache.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            content = f.read().strip()
            if content:
                return json.load(f)
    return {}

def save_translation_cache(cache):
    with open('translation_cache.json', 'w') as f:
        json.dump(cache, f)

def load_flashcards():               
    if os.path.exists(FLASHCARDS_FILE):
        with open(FLASHCARDS_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                return json.load(f)
            else:
                return []
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

        # Auto-group flashcards by meaning with meaningful folder names
        if len(flashcards) > 0:
            translation_cache = load_translation_cache()
            categories = {
                'Animals': ['animal', 'cat', 'dog', 'lion', 'tiger', 'gato', 'perro', 'puppy', 'kitten', 'feline', 'canine'],
                'Food': ['food', 'eat', 'dish', 'meal', 'comida', 'fruit', 'vegetable', 'snack'],
                'Objects': ['thing', 'object', 'tool', 'item', 'furniture', 'chair', 'table'],
                'Uncategorized': []
            }

            new_cards = []
            submitted_words = [line.split(':', 1)[0].strip() for line in request.form['words'].split('\n') if ':' in line]
            for line in request.form['words'].split('\n'):
                if ':' in line:
                    word, meaning = line.split(':', 1)
                    word = word.strip()
                    meaning = meaning.strip()
                    if word not in [card['word'] for card in flashcards]:
                        new_cards.append({'word': word, 'meaning': meaning, 'folder': ''})

            if new_cards:
                flashcards.extend(new_cards)
                save_flashcards(flashcards)

                for card in flashcards:
                    if not card.get('folder'):
                        if card['meaning'] not in translation_cache:
                            translation_cache[card['meaning']] = translator.translate(card['meaning'], dest='en').text
                        translated_meaning = translation_cache[card['meaning']]
                        folder = 'Uncategorized'
                        for cat_name, keywords in categories.items():
                            if any(keyword in translated_meaning.lower() for keyword in keywords):
                                folder = cat_name
                                break
                        card['folder'] = folder

                save_translation_cache(translation_cache)

            save_flashcards(flashcards)

    return render_template('input.html', flashcards=flashcards)

@app.route('/review')
def review():
    flashcards = load_flashcards()
    folders = {}
    for card in flashcards:
        folder = card.get('folder', 'Uncategorized')
        if folder not in folders:
            folders[folder] = []
        folders[folder].append(card)
    return render_template('review.html', folders=folders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
