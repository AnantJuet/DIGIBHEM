from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Function to create database
def create_database():
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            bot_response TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to save conversations
def save_conversation(user_input, bot_response):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (user_input, bot_response) VALUES (?, ?)", (user_input, bot_response))
    conn.commit()
    conn.close()

# Function to get chatbot responses
def get_response(user_input):
    user_input = user_input.lower().strip()  # Normalize input
    
    responses = {
        "hello": "Hi there! How can I help you?",
        "hi": "Hello! How can I assist you?",
        "hey": "Hey! What’s up?",
        "how are you?": "I'm just a bot, but I'm doing great! How about you?",
        "what is your name?": "I'm an AI chatbot designed by Anant to assist you.",
        "what can you do?": "I can answer your questions and chat with you!",
        "bye": "Goodbye! Have a great day!",

        # Maths Questions
        "what is 2 + 2?": "2 + 2 is 4.",
        "what is the square root of 16?": "The square root of 16 is 4.",
        "what is 10 factorial?": "10! (10 factorial) is 3,628,800.",
        "what is the value of pi?": "Pi is approximately 3.14159.",
        "what is pythagoras theorem?": "Pythagoras' theorem states that a² + b² = c² in a right-angled triangle.",

        # Psychology Questions
        "what is cognitive dissonance?": "Cognitive dissonance is the mental discomfort experienced when holding contradictory beliefs.",
        "who is Sigmund Freud?": "Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis.",
        "what is Maslow's hierarchy of needs?": "Maslow's hierarchy of needs is a psychological theory that prioritizes human needs from basic to self-actualization.",
        "what is operant conditioning?": "Operant conditioning is a learning process through rewards and punishments for behavior.",
        "what is a placebo effect?": "The placebo effect occurs when people experience benefits from a treatment that has no active ingredients.",

        # Science Questions
        "what is gravity?": "Gravity is the force that attracts objects with mass towards each other.",
        "what is the speed of light?": "The speed of light in a vacuum is approximately 299,792,458 meters per second.",
        "what is an atom?": "An atom is the smallest unit of matter, consisting of protons, neutrons, and electrons.",
        "what causes earthquakes?": "Earthquakes are caused by the sudden release of energy in the Earth's crust due to tectonic movements.",
        "what is photosynthesis?": "Photosynthesis is the process by which green plants convert sunlight into energy."
    }

    response = responses.get(user_input, "I'm sorry, I don't understand that.")
    save_conversation(user_input, response)  # Save conversation
    return response

# Flask route to serve HTML page
@app.route('/')
def index():
    return render_template("index.html")

# API route to handle chatbot responses
@app.route('/get_response', methods=['POST'])
def chatbot():
    data = request.json
    user_input = data.get("message", "")
    bot_response = get_response(user_input)
    return jsonify({"response": bot_response})

# Run the application
if __name__ == "__main__":
    create_database()  # Ensure database exists
    app.run(debug=True)
