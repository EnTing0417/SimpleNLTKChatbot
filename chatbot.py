# 1. Import necessary libraries
from flask import Flask, request, jsonify, render_template
import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# 2. Initialize Flask app
app = Flask(__name__)

# 3. Define patterns and responses
patterns = [
    {"pattern": r"hi", "responses": ["Hello!", "Hi there!", "Hey!"]},
    {"pattern": r"hello", "responses": ["Hello!", "Hi there!", "Hey!"]},
    {"pattern": r"hey", "responses": ["Hello!", "Hi there!", "Hey!"]},
    {"pattern": r"how are you", "responses": ["I'm doing well, thank you!", "I'm fine, thank you!"]},
    {"pattern": r"what's your name", "responses": ["I'm a chatbot!", "My name is ChatBot!"]},
    # Add more patterns and responses as needed
]

# 4. Preprocess the patterns and responses
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    return [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text)]

nltk.download('punkt')
nltk.download('wordnet')

processed_patterns = [(preprocess_text(pattern["pattern"]), pattern["responses"]) for pattern in patterns]

# 5. Train the chatbot
def chat(message):
    message = preprocess_text(message)
    for pattern, responses in processed_patterns:
        if all(word in message for word in pattern):
            return random.choice(responses)
    return "Sorry, I didn't understand that."

# 6. Define routes for the Flask app
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    data = request.get_json()
    message = data["message"]
    response = chat(message)
    return jsonify({"response": response})

# 7. Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)