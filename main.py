from flask import Flask, request, render_template 
import json
import os
import nltk
from polyglot.detect import Detector  # Offline language detection
from polyglot.text import Text  # Offline translation and analysis
from sentence_transformers import SentenceTransformer  # For semantic embeddings
import numpy as np
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

def get_translation_and_embedding(meaning, model, translation_cache):
    if meaning not in translation_cache:
        try:
            text = Text(meaning)
            if text.languages:
                translated = text.translate('en') if len(text.words) > 0 else meaning
                translation_cache[meaning] = translated
            else:
                translation_cache[meaning] = meaning
        except Exception:
            translation_cache[meaning] = meaning
    translated_meaning = translation_cache[meaning]
    embedding = model.encode(translated_meaning)
    return translated_meaning, embedding

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

        # Auto-group flashcards by meaning with meaningful folder names using embeddings
        if len(flashcards) > 0:
            translation_cache = load_translation_cache()
            model = SentenceTransformer('all-MiniLM-L6-v2')
            categories = {
                'Animals': ['animal', 'cat', 'dog', 'puppy', 'kitten'],
                'Food': ['food', 'eat', 'dish', 'fruit', 'snack'],
                'Objects': ['thing', 'object', 'tool', 'furniture'],
                'Uncategorized': []
            }
            category_embeddings = {}
            for cat_name, keywords in categories.items():
                if keywords:
                    avg_embedding = np.mean([model.encode(keyword) for keyword in keywords], axis=0)
                    category_embeddings[cat_name] = avg_embedding

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
                        translated_meaning, embedding = get_translation_and_embedding(card['meaning'], model, translation_cache)
                        folder = 'Uncategorized'
                        max_similarity = -1
                        for cat_name, cat_embedding in category_embeddings.items():
                            similarity = np.dot(embedding, cat_embedding) / (np.linalg.norm(embedding) * np.linalg.norm(cat_embedding))
                            if similarity > max_similarity:
                                max_similarity = similarity
                                folder = cat_name
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