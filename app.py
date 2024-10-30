from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# נתונים קבועים
initial_agents = [
    {"שם פרטי": "חלי", "שם משפחה": "דיין", "מספר מפנה": "2195"},
    {"שם פרטי": "ויקטור אביחי", "שם משפחה": "פלד", "מספר מפנה": "2421"},
    {"שם פרטי": "אלי", "שם משפחה": "אוחיון", "מספר מפנה": "2422"},
    {"שם פרטי": "אלעד", "שם משפחה": "אלמוג", "מספר מפנה": "2423"},
    {"שם פרטי": "אלעד", "שם משפחה": "אשר", "מספר מפנה": "2424"},
    {"שם פרטי": "אלעד", "שם משפחה": "בן חיים", "מספר מפנה": "2425"},
    {"שם פרטי": "אלעד", "שם משפחה": "דוד", "מספר מפנה": "2426"},
]

# קישורים מוכנים לשליחה - קבועים בקוד
SAVED_LINKS = {
    "2195": [  # קישורים של חלי דיין
        {
            "title": "וובינר פנסיה",
            "text": """🎯 הזמנה לוובינר: תכנון פנסיוני חכם
מה נלמד בוובינר?
✅ איך לבחור את הפנסיה הנכונה
✅ טיפים לחיסכון בדמי ניהול""",
            "post_text": "טקסט נוסף לפוסט",
            "date": "2024-01-01"
        },
        {
            "title": "פגישת ייעוץ",
            "text": """💰 הזמנה לפגישת ייעוץ אישית
בואו נבנה יחד תכנית פיננסית מותאמת אישית""",
            "post_text": "",
            "date": "2024-01-02"
        }
    ],
    "2421": [  # קישורים של ויקטור אביחי פלד
        {
            "title": "וובינר השקעות",
            "text": """💰 הזמנה לוובינר: השקעות חכמות
מה נלמד בוובינר?
✅ בניית תיק השקעות מאוזן
✅ ניהול סיכונים נכון""",
            "post_text": "",
            "date": "2024-01-03"
        }
    ]
}

@app.route('/')
def index():
    return render_template('index.html', 
                         agents=initial_agents,
                         saved_links=SAVED_LINKS)  # העברת הקישורים לתבנית

@app.route('/api/saved-links/<agent_id>', methods=['GET'])
def get_saved_links(agent_id):
    # החזרת הקישורים השמורים לסוכן
    return jsonify(SAVED_LINKS.get(agent_id, []))

@app.route('/api/saved-links/<agent_id>', methods=['POST'])
def add_saved_link(agent_id):
    data = request.json
    if agent_id not in SAVED_LINKS:
        SAVED_LINKS[agent_id] = []
    
    SAVED_LINKS[agent_id].append({
        "title": data.get('title'),
        "text": data.get('text'),
        "post_text": data.get('post_text', ''),
        "date": datetime.now().strftime('%Y-%m-%d')
    })
    
    return jsonify({"message": "Link saved successfully"})

@app.route('/generate_link', methods=['POST'])
def generate_link():
    base_link = request.form.get('link', '')
    agent_id = request.form.get('agent', '')
    free_text = request.form.get('free_text', '')
    
    custom_link = f"{base_link}?ref={agent_id}"
    full_text = f"{free_text}\n\n{custom_link}" if free_text else custom_link
    
    return jsonify({
        'custom_link': custom_link,
        'full_text': full_text,
        'title': 'כותרת לדוגמה',
        'description': 'תיאור לדוגמה',
        'image_url': 'https://example.com/image.jpg'
    })

@app.route('/api/agents', methods=['POST'])
def add_agent():
    try:
        data = request.json
        new_agent = {
            "שם פרטי": data['first_name'],
            "שם משפחה": data['last_name'],
            "מספר מפנה": data['referral_id']
        }
        initial_agents.append(new_agent)
        return jsonify({"message": "Agent added successfully", "agent": new_agent})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    try:
        global initial_agents
        initial_agents = [agent for agent in initial_agents if agent['מספר מפנה'] != agent_id]
        return jsonify({"message": "Agent deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)