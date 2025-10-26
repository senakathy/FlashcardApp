# 📚 FlashLearn Code Explanation
## Complete Guide to Understanding Every Part of the Code

---

## 📁 Project Structure

```
FlashLearn/
├── main.py                    # Flask backend (Python server)
├── flashcards_data.json       # Storage file for all flashcards and folders
├── static/                    # CSS and JavaScript files
│   ├── kpop-simple.css       # Purple theme stylesheet
│   └── sounds.js             # Sound effect functions
└── templates/                # HTML pages
    ├── landing.html          # Purple welcome page
    ├── input.html            # Add flashcards page
    ├── my-flashcards.html    # Manage flashcards page
    └── review.html           # Study/review page
```

---

## 🐍 MAIN.PY - The Python Backend

### Overview
This file runs the web server and handles all the logic for saving, loading, and moving flashcards.

### Key Concepts

**Flask** = A Python framework that lets you create websites
**Route** = A URL path (like /home or /review) that shows a different page
**JSON** = A file format for storing data (like a dictionary saved to a file)

### Functions Explained

#### 1. load_data()
```python
def load_data():
    if os.path.exists(DATA_FILE):          # Check if file exists
        with open(DATA_FILE, 'r') as f:    # Open in read mode
            content = f.read().strip()      # Read all text
            if content:                     # If not empty
                return json.loads(content)  # Convert JSON text to Python dict
    return {'folders': [], 'uncategorized': []}  # Default empty structure
```
**What it does:** Loads all your flashcards and folders from the JSON file.
**Returns:** A dictionary with two parts:
- `folders`: List of folder objects
- `uncategorized`: List of flashcards not in any folder

#### 2. save_data(data)
```python
def save_data(data):
    with open(DATA_FILE, 'w') as f:        # Open in write mode
        json.dump(data, f, indent=2)        # Save dict as formatted JSON
```
**What it does:** Saves all flashcards and folders to the JSON file.
**Parameter:** `data` - the complete dictionary of flashcards and folders

#### 3. get_all_flashcards()
```python
def get_all_flashcards():
    data = load_data()                      # Load everything
    all_cards = data['uncategorized'].copy()  # Start with uncategorized
    for folder in data['folders']:          # Loop through folders
        all_cards.extend(folder['flashcards'])  # Add each folder's cards
    return all_cards                        # Return combined list
```
**What it does:** Combines flashcards from all folders into one big list.
**Used for:** The "Review All" feature.

### Routes Explained

#### Route: / (Landing Page)
```python
@app.route('/')
def index():
    return render_template('landing.html')
```
- **URL:** `http://localhost:5000/`
- **Shows:** Purple welcome page with lightning bolt
- **Method:** GET only

#### Route: /home (Add Flashcards)
```python
@app.route('/home', methods=['GET', 'POST'])
def home():
    # GET: Show the form
    # POST: Process new flashcards
```
- **URL:** `http://localhost:5000/home`
- **Shows:** Form to add flashcards
- **GET:** Displays the page
- **POST:** When you click "Add Words", processes the flashcards

**How it processes flashcards:**
1. Splits textarea by newlines (`\n`) to get individual lines
2. For each line with a colon (`word:meaning`):
   - Splits at the colon
   - Creates a dictionary: `{'word': 'cat', 'meaning': 'feline animal'}`
   - Adds to selected folder or uncategorized
3. Saves everything to JSON file

#### Route: /review (Study Page)
```python
@app.route('/review', methods=['GET', 'POST'])
def review():
    # GET: Show folder selection
    # POST: Show review interface with selected cards
```
- **GET:** Shows checkboxes to pick folders and review mode
- **POST:** Shows the actual flashcards to study

**How folder selection works:**
```python
selected_folders = request.form.getlist('selected_folders')
# Returns a list like: ['all'] or ['uncategorized', 'folder-uuid-123']

if 'all' in selected_folders:
    flashcards = get_all_flashcards()  # Get everything
else:
    # Build list from selected folders only
```

#### Route: /move-flashcard (Move Cards Between Folders)
```python
@app.route('/move-flashcard', methods=['POST'])
def move_flashcard():
    # 1. Get which card (index), from where, to where
    # 2. Remove from source (using .pop())
    # 3. Add to destination (using .append())
    # 4. Save changes
```

**How .pop() works:**
```python
my_list = ['apple', 'banana', 'orange']
removed = my_list.pop(1)  # Removes and returns 'banana'
# Now my_list = ['apple', 'orange']
```

---

## 🎨 STATIC/KPOP-SIMPLE.CSS - The Purple Theme

### CSS Basics

**Selector** = Which elements to style (e.g., `h1`, `.btn`, `#quiz-input`)
**Property** = What to change (e.g., `color`, `font-size`, `padding`)
**Value** = The new setting (e.g., `#6a1b9a`, `16px`, `10px`)

### Example Breakdown
```css
.btn-primary {
    background: #6a1b9a;     /* Purple background */
    color: white;            /* White text */
}

.btn-primary:hover {         /* :hover = when mouse is over it */
    background: #5a168a;     /* Darker purple */
    transform: translateY(-1px);  /* Move up 1 pixel */
}
```

### Important CSS Concepts

**Box Model:**
```
┌─────────────────────────────────┐
│         Margin (outside)         │
│  ┌───────────────────────────┐  │
│  │   Border                   │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  Padding            │  │  │
│  │  │  ┌───────────────┐  │  │  │
│  │  │  │   Content     │  │  │  │
│  │  │  └───────────────┘  │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

**Colors:**
- `#6a1b9a` = Deep purple (hex code: red=6a, green=1b, blue=9a)
- `rgba(106, 27, 154, 0.1)` = Purple with 10% opacity
- Alpha (last number) = transparency (0 = invisible, 1 = solid)

**Flexbox (for centering):**
```css
display: flex;              /* Use flexbox layout */
justify-content: center;    /* Center horizontally */
align-items: center;        /* Center vertically */
```

---

## 🔊 STATIC/SOUNDS.JS - Sound Effects

### How Web Audio Works

**Web Audio API** = Browser's built-in sound generator
**No audio files needed!** - All sounds are created with code

### Creating a Simple Beep
```javascript
// 1. Create audio context (the "sound factory")
const audioContext = new AudioContext();

// 2. Create oscillator (makes tones)
const oscillator = audioContext.createOscillator();

// 3. Create gain node (controls volume)
const gainNode = audioContext.createGain();

// 4. Connect them: oscillator → gain → speakers
oscillator.connect(gainNode);
gainNode.connect(audioContext.destination);

// 5. Configure
oscillator.frequency.value = 1000;  // 1000 Hz = high pitch
gainNode.gain.value = 0.1;          // Quiet (10% volume)

// 6. Play
oscillator.start();                 // Start now
oscillator.stop(audioContext.currentTime + 0.1);  // Stop after 0.1 sec
```

### How the Whoosh Sound Works

1. **Create white noise** - random values between -1 and 1
2. **Apply fade** - multiply by decreasing curve (loud → quiet)
3. **Filter** - only allow middle frequencies through
4. **Sweep** - change filter from high to low frequency
5. **Result** - sounds like "whoooosh"

```javascript
// Generate random noise that fades out
for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1)    // Random: -1 to 1
              * Math.pow(1 - i/bufferSize, 2);  // Fade curve
}
```

---

## 🌐 HTML TEMPLATES - The Web Pages

### Jinja2 Template Language

Flask uses Jinja2 to put Python data into HTML.

**Syntax:**
- `{{ variable }}` - Print a value
- `{% for item in list %}` - Start a loop
- `{% endfor %}` - End the loop
- `{% if condition %}` - Start a condition
- `{% endif %}` - End the condition

**Example:**
```html
<!-- Python sends: folders = [{'name': 'Family'}, {'name': 'School'}] -->

{% for folder in folders %}
    <option value="{{ folder.id }}">{{ folder.name }}</option>
{% endfor %}

<!-- Result HTML: -->
<option value="uuid-123">Family</option>
<option value="uuid-456">School</option>
```

### LANDING.HTML

**Purpose:** Welcome screen with animated logo

**Key Features:**
1. **Gradient background** - Created with CSS linear-gradient
2. **SVG lightning bolt** - Vector graphic (scales perfectly)
3. **Pulse animation** - Logo grows/shrinks with @keyframes
4. **Glassmorphism** - Blurred transparent boxes for features

**How the gradient works:**
```css
background: linear-gradient(135deg, #6a1b9a 0%, #8e24aa 50%, #ab47bc 100%);
```
- `135deg` = Diagonal angle
- Color stops: Dark purple → Medium purple → Light purple

### INPUT.HTML

**Purpose:** Add new flashcards

**How folder dropdown works:**
```html
<select name="folder_id" id="folder_select">
    <option value="">Uncategorized</option>
    {% for folder in folders %}
        <option value="{{ folder.id }}">{{ folder.name }}</option>
    {% endfor %}
    <option value="new_folder">+ Create New Folder</option>
</select>
```

**JavaScript for showing/hiding new folder input:**
```javascript
document.getElementById('folder_select').addEventListener('change', function() {
    // Get the hidden input div
    const newFolderInput = document.getElementById('new_folder_input');
    
    // If user selected "Create New Folder"
    if (this.value === 'new_folder') {
        newFolderInput.style.display = 'block';  // Show it
    } else {
        newFolderInput.style.display = 'none';   // Hide it
    }
});
```

### MY-FLASHCARDS.HTML

**Purpose:** Manage and organize flashcards

**Features:**
1. **Collapsible folders** - Click to expand/collapse
2. **Drag and drop** - Drag cards to different folders
3. **Move button** - Two-step move (click Move → select folder → Confirm)
4. **Delete** - Remove cards or folders

**How collapsible folders work:**

CSS:
```css
.folder-cards {
    display: none;  /* Hidden by default */
}

.folder-cards.active {
    display: block;  /* Shown when active class added */
}
```

JavaScript:
```javascript
function toggleFolder(element) {
    // Find the arrow and cards container
    const arrow = element.querySelector('.dropdown-arrow');
    const folderCards = element.closest('.folder-section')
                               .querySelector('.folder-cards');
    
    // Toggle arrow rotation
    arrow.classList.toggle('rotated');  // Adds/removes 'rotated' class
    
    // Toggle cards visibility
    folderCards.classList.toggle('active');  // Adds/removes 'active' class
}
```

**How drag-and-drop works:**

1. **Mark as draggable:**
```html
<div draggable="true" 
     data-index="0" 
     data-from-folder="uuid-123"
     ondragstart="handleDragStart(event)">
```

2. **Start dragging:**
```javascript
function handleDragStart(event) {
    draggedCard = event.target;  // Remember which card
    draggedCard.classList.add('dragging');  // Add visual effect
}
```

3. **Drag over folder:**
```javascript
function handleDragOver(event) {
    event.preventDefault();  // Allow dropping
    event.currentTarget.classList.add('drag-over');  // Purple highlight
}
```

4. **Drop the card:**
```javascript
function handleDrop(event) {
    const fromFolder = draggedCard.getAttribute('data-from-folder');
    const toFolder = event.currentTarget.getAttribute('data-folder-id');
    const cardIndex = draggedCard.getAttribute('data-index');
    
    // Create and submit a form to move the card
    // (Forms are how we send data to Python)
}
```

### REVIEW.HTML

**Purpose:** Study flashcards with two modes

**Two Review Modes:**

1. **Flip Mode:**
```html
<div class="flashcard" onclick="flipCard(this)">
    <div class="card-inner">
        <div class="card-front">{{ word }}</div>
        <div class="card-back">{{ meaning }}</div>
    </div>
</div>
```

CSS for 3D flip:
```css
.card-inner {
    transform-style: preserve-3d;  /* Enable 3D */
    transition: transform 0.6s;     /* Smooth animation */
}

.flipped .card-inner {
    transform: rotateY(180deg);     /* Flip 180 degrees */
}
```

2. **Quiz Mode:**
```html
<p id="quiz-meaning">{{ meaning }}</p>
<input type="text" id="quiz-input" placeholder="Type the word...">
<button onclick="checkAnswer()">Check Answer</button>
```

**How answer checking works:**
```javascript
function checkAnswer() {
    const userAnswer = document.getElementById('quiz-input').value
                              .trim()       // Remove spaces
                              .toLowerCase(); // Make lowercase
    
    const correctAnswer = flashcards[currentIndex].word.toLowerCase();
    
    if (userAnswer === correctAnswer) {
        // Show green success message
        result.innerHTML = '<div class="alert alert-success">✓ Correct!</div>';
    } else {
        // Show red error message with correct answer
        result.innerHTML = '<div class="alert alert-danger">✗ Incorrect. Answer: ' + 
                          flashcards[currentIndex].word + '</div>';
    }
}
```

**How shuffle works:**

Fisher-Yates algorithm (randomly rearranges array):
```javascript
function shuffleCards() {
    // Loop backwards through array
    for (let i = flashcards.length - 1; i > 0; i--) {
        // Pick random position from 0 to i
        const j = Math.floor(Math.random() * (i + 1));
        
        // Swap positions i and j
        [flashcards[i], flashcards[j]] = [flashcards[j], flashcards[i]];
    }
    
    currentIndex = 0;  // Go back to first card
    updateCard();      // Display the first card
}
```

---

## 🎯 DATA FLOW - How Everything Connects

### Adding a Flashcard

```
1. User types in textarea:
   "dog:canine pet"

2. User clicks "Add Words"
   ↓
3. Browser sends POST request to /home:
   words="dog:canine pet"
   folder_id="uuid-123"

4. Python (main.py) receives it:
   word_list = request.form['words'].split('\n')
   → ['dog:canine pet']
   
5. Python splits by colon:
   word, meaning = 'dog:canine pet'.split(':', 1)
   → word='dog', meaning='canine pet'

6. Python creates dictionary:
   new_card = {'word': 'dog', 'meaning': 'canine pet'}

7. Python adds to folder:
   folder['flashcards'].append(new_card)

8. Python saves to JSON file:
   save_data(data)

9. Page reloads, showing updated form
```

### Reviewing Flashcards

```
1. User visits /review
   ↓
2. Python shows folder selection form

3. User checks "Family" and "Quiz Mode"
   ↓
4. Browser sends POST:
   selected_folders=['uuid-123']
   review_mode='quiz'

5. Python gathers flashcards:
   flashcards = []
   for folder_id in selected_folders:
       flashcards.extend(folder['flashcards'])

6. Python renders review.html:
   - Passes flashcards array
   - Passes review_mode='quiz'

7. JavaScript receives data:
   const flashcards = [
       {'word': 'mother', 'meaning': 'female parent'},
       {'word': 'father', 'meaning': 'male parent'}
   ];

8. Quiz mode shows:
   - Meaning: "female parent"
   - Input: [type answer here]

9. User types "mother" and clicks Check
   ↓
10. JavaScript compares:
    'mother' === 'mother' → Correct! ✓
```

---

## 🔑 KEY PROGRAMMING CONCEPTS

### 1. HTTP Methods

**GET** = Retrieve data (just looking, not changing anything)
- Example: Load the add flashcards page

**POST** = Send data (making changes, adding/moving/deleting)
- Example: Submit new flashcards

### 2. JSON Data Structure

```json
{
  "folders": [
    {
      "id": "uuid-abc-123",
      "name": "Family",
      "flashcards": [
        {"word": "mother", "meaning": "female parent"},
        {"word": "father", "meaning": "male parent"}
      ]
    }
  ],
  "uncategorized": [
    {"word": "cat", "meaning": "feline animal"}
  ]
}
```

### 3. Event Listeners

JavaScript "listens" for user actions:

```javascript
button.addEventListener('click', function() {
    // This code runs when button is clicked
    playSound();
});
```

### 4. Form Submission

HTML form:
```html
<form method="POST" action="/create-folder">
    <input name="folder_name" value="School">
    <button type="submit">Create</button>
</form>
```

When submitted, browser sends:
```
POST /create-folder
folder_name=School
```

Python receives it:
```python
folder_name = request.form.get('folder_name')
# folder_name = 'School'
```

### 5. CSS Transitions

Smooth changes over time:

```css
.btn {
    background: white;
    transition: all 0.3s ease;  /* Animate all changes over 0.3 seconds */
}

.btn:hover {
    background: purple;  /* This change will be smooth/gradual */
}
```

---

## 🐛 DEBUGGING TIPS

### If flashcards don't save:
1. Check that `flashcards_data.json` file exists
2. Look at Python console for error messages
3. Make sure the form is using `method="POST"`

### If sounds don't play:
1. Check browser console (F12) for errors
2. Make sure `sounds.js` is loaded
3. Try clicking somewhere first (browsers block audio until user interaction)

### If CSS doesn't apply:
1. Check that `kpop-simple.css` is loaded (view page source)
2. Clear browser cache (Ctrl+Shift+R)
3. Make sure class names match exactly

### If drag-and-drop doesn't work:
1. Check that `draggable="true"` is set
2. Make sure all event handlers are attached
3. Look for JavaScript errors in console

---

## 📖 FURTHER LEARNING

**Flask:**
- Official tutorial: https://flask.palletsprojects.com/tutorial/
- Learn: routes, templates, forms

**JavaScript:**
- MDN Web Docs: https://developer.mozilla.org/en-US/docs/Web/JavaScript
- Learn: functions, events, DOM manipulation

**CSS:**
- CSS Tricks: https://css-tricks.com/
- Learn: flexbox, animations, responsive design

**Web Audio:**
- MDN Guide: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- Learn: oscillators, gain nodes, filters

---

## 🎓 SUMMARY

**Backend (Python):**
- Flask handles routing (which page to show for each URL)
- Data is stored in JSON file
- Each route either shows a page or processes data

**Frontend (HTML/CSS/JavaScript):**
- HTML structures the page
- CSS makes it look pretty with purple theme
- JavaScript adds interactivity (sounds, animations, drag-drop)

**Data Flow:**
- User action → Browser sends request → Python processes → Saves to JSON
- User visits page → Python loads JSON → Sends to HTML template → Shows page

**Key Features:**
- Folder organization with drag-and-drop
- Two review modes (flip and quiz)
- Sound effects generated with Web Audio
- Purple K-Pop inspired design theme
- Everything stored in one JSON file (no database needed!)

---

*This guide explains every major part of the FlashLearn application. Use it as a reference when you want to understand or modify the code!*
