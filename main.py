from flask import Flask, request, render_template 
import  json #a type of file that stores data in a dictionary format
import os #helps pythn interact with the operating system to check if a file exists for example.
import nltk # Natural Language Toolkit
from sklearn.feature_extraction.text import TfidfVectorizer #converts text into numerical data
from sklearn.cluster import KMeans #helps group similar words together

nltk.download('punkt', quiet=True)  # Download text splitter (runs once)
app = Flask(__name__)                # python library that helps create applications
FLASHCARDS_FILE = 'flashcards.json'  # give the file a variable name

def load_flashcards():               
  if os.path.exists(FLASHCARDS_FILE):     # if this file exists
    with open(FLASHCARDS_FILE, 'r') as f: # open the file in read mode and give it a variable name 
      return json.load(f)                 # return the data in the file
  return []                               # if the file doesn't exist, return an empty list

def save_flashcards(flashcards):          
    with open(FLASHCARDS_FILE, 'w') as f:   # open the file in write mode and give it a variable
      json.dump(flashcards,f)                # write the new data(flashcards) into the file. 

@app.route('/', methods = ['GET', 'POST']) # when the home page is loaded, 
def index():
  flashcards = load_flashcards()           # put all the data in the file into a variaavle called flashcards
  if request.method == 'POST':             #if the user submits a form then 
      word_list = request.form['words'].split('\n') # split the words enteterd into a list based on the new line
      for line in word_list:                         
          if ':' in line:                #if the line has a colon, separate the word and meaning
              word, meaning = line.split(':',1)
              flashcards.append({'word': word.strip(), 'meaning': meaning.strip(), 'folder': ''}) #add the new word

      save_flashcards(flashcards) #save all the data(old and new) into the FLASHCARDS_FILE
      # Auto-group flashcards by meaning (only if more than 1 card)
      if len(flashcards) > 1:
          meanings = [card['meaning'] for card in flashcards]  # Get all meanings
          vectorizer = TfidfVectorizer(stop_words='english')  # Turn text to numbers 
          X = vectorizer.fit_transform(meanings)  # Fit and transform meanings to numbers
          k = min(3, len(flashcards))  # Number of groups (up to 3)
          kmeans = KMeans(n_clusters=k, random_state=0).fit(X)  # Group the numbers
          for i, card in enumerate(flashcards):
              card['folder'] = f"Group_{kmeans.labels_[i]}"  # Assign group name to card
          save_flashcards(flashcards)  # Save with folders
  return render_template('input.html', flashcards = flashcards)  

@app.route('/review')
def review():
  flashcards = load_flashcards()
  return render_template('review.html', flashcards=flashcards)


if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 8080)
  





