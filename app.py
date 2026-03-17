from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import os
from database import init_db, save_score, get_top_scores, save_chat

# Naloži .env datoteko (Load .env file)
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Poveži z Google Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Inicializiraj bazo podatkov (Initialize database)
init_db()

# Prikaži igro (Serve the game)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# AI Chat
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    user = data.get('user', 'Gost')

    if not message:
        return jsonify({'error': 'Sporočilo je prazno'}), 400

    try:
        response = model.generate_content(message)
        reply = response.text
        save_chat(user, message, reply)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Shrani rezultat (Save score)
@app.route('/api/score', methods=['POST'])
def score():
    data = request.get_json()
    name = data.get('name', 'Neznan')
    points = data.get('points', 0)
    save_score(name, points)
    return jsonify({'success': True})

# Pridobi lestvico (Get leaderboard)
@app.route('/api/scores', methods=['GET'])
def scores():
    return jsonify(get_top_scores())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)