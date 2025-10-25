# Auto-group flashcards by meaning with meaningful folder names using embeddings
if len(flashcards) > 0:  # Group even with 1 card for consistency
    # Load or initialize translation cache
    translation_cache = load_translation_cache()
    # Initialize embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Define category keywords with some exemplars
    categories = {
        'Animals': ['animal', 'cat', 'dog', 'puppy', 'kitten'],
        'Food': ['food', 'eat', 'dish', 'fruit', 'snack'],
        'Objects': ['thing', 'object', 'tool', 'furniture'],
        'Uncategorized': []
    }
    # Pre-compute category embeddings
    category_embeddings = {}
    for cat_name, keywords in categories.items():
        if keywords:  # Only compute for non-empty categories
            avg_embedding = np.mean([model.encode(keyword) for keyword in keywords], axis=0)
            category_embeddings[cat_name] = avg_embedding

    # Process new cards from this submission, avoiding duplicates
    new_cards = []
    submitted_words = [line.split(':', 1)[0].strip() for line in request.form['words'].split('\n') if ':' in line]
    for line in request.form['words'].split('\n'):
        if ':' in line:
            word, meaning = line.split(':', 1)
            word = word.strip()
            meaning = meaning.strip()
            if word not in [card['word'] for card in flashcards]:
                new_cards.append({'word': word, 'meaning': meaning, 'folder': ''})

    if new_cards:  # If new cards were added
        flashcards.extend(new_cards)  # Add new cards to the list
        save_flashcards(flashcards)  # Save before grouping

        # Assign folders to new cards using embeddings
        for card in flashcards:
            if not card.get('folder'):  # Only process cards without a folder
                translated_meaning, embedding = get_translation_and_embedding(card['meaning'], model, translation_cache)
                folder = 'Uncategorized'
                max_similarity = -1
                for cat_name, cat_embedding in category_embeddings.items():
                    similarity = np.dot(embedding, cat_embedding) / (np.linalg.norm(embedding) * np.linalg.norm(cat_embedding))
                    if similarity > max_similarity:
                        max_similarity = similarity
                        folder = cat_name
                card['folder'] = folder

        save_translation_cache(translation_cache)  # Save updated cache

    save_flashcards(flashcards)  # Save final state