# Import necessary libraries for the Flask web application
from flask import Flask, request, render_template, redirect, url_for, jsonify  # Flask web framework tools
import json  # For reading and writing JSON files
import os  # For checking if files exist
import nltk  # Natural Language Toolkit (kept for potential future use)
import uuid  # For generating unique IDs for folders

# Download NLTK data quietly (runs once, kept for potential future use)
nltk.download('punkt', quiet=True)

# Initialize the Flask application - this creates our web app
app = Flask(__name__)

# Define the file where all flashcard data is stored
DATA_FILE = 'flashcards_data.json'

# ============================================================================
# HELPER FUNCTIONS - These help manage data storage and retrieval
# ============================================================================

def load_data():
    """
    Load all flashcard data from the JSON file.
    Returns a dictionary with 'folders' and 'uncategorized' flashcards.
    If the file doesn't exist, returns empty data structure.
    """
    # Check if the data file exists on the computer
    if os.path.exists(DATA_FILE):
        # Open the file in read mode
        with open(DATA_FILE, 'r') as f:
            # Read all the content from the file
            content = f.read().strip()
            # If there's actually content in the file
            if content:
                # Convert JSON text to Python dictionary and return it
                return json.loads(content)
    # If file doesn't exist or is empty, return default empty structure
    return {'folders': [], 'uncategorized': []}

def save_data(data):
    """
    Save all flashcard data to the JSON file.
    Takes a dictionary and writes it to flashcards_data.json
    """
    # Open the file in write mode (creates it if it doesn't exist)
    with open(DATA_FILE, 'w') as f:
        # Convert Python dictionary to JSON and write it
        # indent=2 makes the JSON file readable with nice formatting
        json.dump(data, f, indent=2)

def migrate_old_data():
    """
    Migrate data from old flashcards.json format to new structure.
    This helps users who had the old version of the app.
    Returns the current data.
    """
    # Check if old file exists but new file doesn't
    if os.path.exists('flashcards.json') and not os.path.exists(DATA_FILE):
        # Open the old flashcards file
        with open('flashcards.json', 'r') as f:
            content = f.read().strip()
            # If there's content in the old file
            if content:
                # Load the old flashcards
                old_flashcards = json.loads(content)
                # Create new data structure with old flashcards in 'uncategorized'
                new_data = {'folders': [], 'uncategorized': old_flashcards}
                # Save it in the new format
                save_data(new_data)
                return new_data
    # If no migration needed, just load current data
    return load_data()

def get_all_flashcards():
    """
    Get all flashcards from all folders combined.
    Used for the "Review All" feature.
    Returns a list of all flashcard dictionaries.
    """
    # Load all the data
    data = load_data()
    # Start with a copy of uncategorized flashcards
    all_cards = data['uncategorized'].copy()
    # Loop through each folder
    for folder in data['folders']:
        # Add all flashcards from this folder to our list
        all_cards.extend(folder['flashcards'])
    # Return the combined list
    return all_cards

# ============================================================================
# ROUTES - These define what happens when you visit different URLs
# ============================================================================

@app.route('/')
def index():
    """
    Landing page route - the first page you see when you open the app.
    Shows the purple welcome page with the lightning bolt logo.
    """
    # Render and return the landing page HTML template
    return render_template('landing.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    Main page for adding flashcards.
    GET: Shows the form to add flashcards
    POST: Processes new flashcards and saves them
    """
    # Load data and migrate old format if needed
    data = migrate_old_data()
    
    # If the user submitted the form (clicked "Add Words")
    if request.method == 'POST':
        # Get the text from the textarea and split it into lines
        word_list = request.form['words'].split('\n')
        # Get which folder was selected (empty string if Uncategorized)
        folder_id = request.form.get('folder_id', '')
        # Get the new folder name if user wants to create one
        new_folder_name = request.form.get('new_folder_name', '').strip()
        
        # Create new folder if user selected "Create New Folder" and entered a name
        if folder_id == 'new_folder' and new_folder_name:
            # Create a new folder dictionary
            new_folder = {
                'id': str(uuid.uuid4()),  # Generate unique ID
                'name': new_folder_name,  # Use the name they entered
                'flashcards': []  # Start with empty flashcards list
            }
            # Add the new folder to our data
            data['folders'].append(new_folder)
            # Update folder_id to point to this new folder
            folder_id = new_folder['id']
        
        # Process each line of input (each flashcard)
        for line in word_list:
            # Only process lines that have a colon (word:meaning format)
            if ':' in line:
                # Split the line at the first colon
                word, meaning = line.split(':', 1)
                # Create a flashcard dictionary with cleaned up text
                new_card = {'word': word.strip(), 'meaning': meaning.strip()}
                
                # If a specific folder was selected
                if folder_id and folder_id != 'new_folder':
                    # Find the folder and add the card to it
                    for folder in data['folders']:
                        if folder['id'] == folder_id:
                            folder['flashcards'].append(new_card)
                            break  # Stop searching once we found it
                else:
                    # No folder selected, add to uncategorized
                    data['uncategorized'].append(new_card)
        
        # Save all changes to the file
        save_data(data)
    
    # Render the input page with the list of folders
    # This shows the form whether it's GET or POST
    return render_template('input.html', folders=data['folders'])

@app.route('/review', methods=['GET', 'POST'])
def review():
    """
    Review page - where you study your flashcards.
    GET: Shows folder and mode selection
    POST: Shows the actual review interface with selected flashcards
    """
    # Load all flashcard data
    data = load_data()
    
    # If user submitted the selection form (clicked "Start Review")
    if request.method == 'POST':
        # Get all selected folder checkboxes (returns a list)
        selected_folders = request.form.getlist('selected_folders')
        # Get which review mode they chose (flip or quiz)
        review_mode = request.form.get('review_mode', 'flip')
        # Start with empty flashcards list
        flashcards = []
        
        # If "All Flashcards" was checked
        if 'all' in selected_folders:
            # Get every flashcard from everywhere
            flashcards = get_all_flashcards()
        else:
            # User selected specific folders
            # If Uncategorized was checked
            if 'uncategorized' in selected_folders:
                # Add all uncategorized flashcards
                flashcards.extend(data['uncategorized'])
            
            # Loop through each selected folder ID
            for folder_id in selected_folders:
                # Skip 'uncategorized' since we already handled it
                if folder_id != 'uncategorized':
                    # Find this folder in our data
                    for folder in data['folders']:
                        if folder['id'] == folder_id:
                            # Add all flashcards from this folder
                            flashcards.extend(folder['flashcards'])
                            break  # Stop searching once found
        
        # Start at the first flashcard
        current_index = 0
        # Show the review page with the selected flashcards
        return render_template('review.html', 
                             flashcards=flashcards,  # The cards to review
                             current_index=current_index,  # Which card to show first
                             folders=data['folders'],  # All folders (for reference)
                             show_selection=False,  # Hide the selection form
                             review_mode=review_mode)  # Which mode (flip or quiz)
    
    # GET request - show the folder selection screen
    return render_template('review.html', 
                         flashcards=[],  # No flashcards yet
                         current_index=0,  # Start at 0
                         folders=data['folders'],  # Show all folders
                         show_selection=True)  # Show the selection form

@app.route('/my-flashcards')
def my_flashcards():
    """
    Page that shows all your flashcards organized in folders.
    You can manage, move, and delete flashcards here.
    """
    # Load all data
    data = load_data()
    # Render the page with folders and uncategorized flashcards
    return render_template('my-flashcards.html', 
                         folders=data['folders'],  # All folders with their cards
                         uncategorized=data['uncategorized'])  # Uncategorized cards

@app.route('/create-folder', methods=['POST'])
def create_folder():
    """
    Creates a new empty folder.
    Called when user types a folder name and clicks "Create Folder".
    """
    # Load current data
    data = load_data()
    # Get the folder name from the form and remove extra spaces
    folder_name = request.form.get('folder_name', '').strip()
    
    # Only create folder if a name was provided
    if folder_name:
        # Create new folder dictionary
        new_folder = {
            'id': str(uuid.uuid4()),  # Unique ID
            'name': folder_name,  # The name user entered
            'flashcards': []  # Start empty
        }
        # Add it to the folders list
        data['folders'].append(new_folder)
        # Save to file
        save_data(data)
    
    # Go back to the My Flashcards page
    return redirect(url_for('my_flashcards'))

@app.route('/move-flashcard', methods=['POST'])
def move_flashcard():
    """
    Moves a flashcard from one folder to another.
    Used when you drag-and-drop or use the Move button.
    """
    # Load current data
    data = load_data()
    # Get which flashcard to move (its position in the list)
    flashcard_index = int(request.form.get('flashcard_index', 0))
    # Get where it's coming from
    from_folder = request.form.get('from_folder', '')
    # Get where it's going to
    to_folder = request.form.get('to_folder', '')
    
    # If no destination was selected, don't do anything
    if not to_folder:
        return redirect(url_for('my_flashcards'))
    
    # Find and remove the flashcard from its current location
    flashcard = None  # Will hold the flashcard we're moving
    
    # If it's coming from uncategorized
    if from_folder == 'uncategorized':
        # Make sure the index is valid
        if flashcard_index < len(data['uncategorized']):
            # Remove it from uncategorized and save it
            flashcard = data['uncategorized'].pop(flashcard_index)
    else:
        # It's in a folder, so find that folder
        for folder in data['folders']:
            if folder['id'] == from_folder:
                # Make sure the index is valid
                if flashcard_index < len(folder['flashcards']):
                    # Remove it from this folder
                    flashcard = folder['flashcards'].pop(flashcard_index)
                break  # Found it, stop looking
    
    # Add the flashcard to its new location
    if flashcard:  # Make sure we actually found a flashcard
        # If moving to uncategorized
        if to_folder == 'uncategorized':
            data['uncategorized'].append(flashcard)
        else:
            # Moving to a specific folder
            for folder in data['folders']:
                if folder['id'] == to_folder:
                    # Add it to this folder
                    folder['flashcards'].append(flashcard)
                    break  # Found it, stop looking
    
    # Save all changes
    save_data(data)
    # Go back to My Flashcards page
    return redirect(url_for('my_flashcards'))

@app.route('/delete-flashcard', methods=['POST'])
def delete_flashcard():
    """
    Deletes a flashcard permanently.
    Called when you click the Delete button on a flashcard.
    """
    # Load current data
    data = load_data()
    # Get which flashcard to delete
    flashcard_index = int(request.form.get('flashcard_index', 0))
    # Get which folder it's in
    from_folder = request.form.get('from_folder', '')
    
    # Remove the flashcard from its location
    if from_folder == 'uncategorized':
        # It's in uncategorized
        if flashcard_index < len(data['uncategorized']):
            # Delete it from the list
            data['uncategorized'].pop(flashcard_index)
    else:
        # It's in a folder
        for folder in data['folders']:
            if folder['id'] == from_folder:
                # Make sure index is valid
                if flashcard_index < len(folder['flashcards']):
                    # Delete it from this folder
                    folder['flashcards'].pop(flashcard_index)
                break  # Found it, stop looking
    
    # Save changes
    save_data(data)
    # Go back to My Flashcards page
    return redirect(url_for('my_flashcards'))

@app.route('/delete-folder/<folder_id>', methods=['POST'])
def delete_folder(folder_id):
    """
    Deletes a folder and moves its flashcards to Uncategorized.
    Called when you click Delete on a folder.
    """
    # Load current data
    data = load_data()
    
    # Loop through folders to find the one to delete
    for i, folder in enumerate(data['folders']):
        if folder['id'] == folder_id:
            # Before deleting, move all its flashcards to uncategorized
            # So we don't lose the flashcards
            data['uncategorized'].extend(folder['flashcards'])
            # Delete the folder from the list
            data['folders'].pop(i)
            break  # Found and deleted it, stop looking
    
    # Save changes
    save_data(data)
    # Go back to My Flashcards page
    return redirect(url_for('my_flashcards'))

# ============================================================================
# RUN THE APPLICATION
# ============================================================================

if __name__ == '__main__':
    """
    This runs when you execute 'python main.py'
    Starts the Flask web server on port 5000
    """
    # Run the app:
    # - host='0.0.0.0' means accessible from any computer on the network
    # - port=5000 means visit the app at http://localhost:5000
    app.run(host='0.0.0.0', port=5000)
