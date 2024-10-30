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
            "title": "מטרות ויעדים למשק הבית",
            "text": """מטרות ויעדים למשק הבית
29.10.2024

https://goola-group.com/webinars/niv-20-10-24/?refferer_id=xxx&target=yyy""",
            "post_text": """תדמיינו שנכנסתם לרכב, לחצתם על הוויז וביקשתם ממנו מסלול בלי להזין כתובת.
בלי יעד הוויז לא יודע לתת לנו מסלול.
כך בדיוק גם בחיים, כשאתם לא מגדירים לכם יעדים ברורים, קשה להגדיר את המסלול כדי לעמוד ביעד.
במפגש הקרוב תגלו איך הגדרת מטרות ויעדים ישפרו באופן ניכר את העתיד הכלכלי שלכם.""",
            "date": "2024-01-01"
        },
        {
            "title": "האתגר הפנסיוני בעולם המערבי",
            "text": """האתגר הפנסיוני בעולם המערבי
29.10.2024

https://goola-group.com/webinars/kobi-20-11-24/?refferer_id=xxx&target=yyy""",
            "post_text": """מי מאיתנו לא מדמיין את תקופת הפנסיה, טיולים סביב העולם, עזרה לילדים, בילוי עם הנכדים בקיצור הרבה זמן פנוי שמחייב הכנסה משמעותית.
אז איך תבטיחו לעצמכם הכנסה גבוהה? 
אילו אתגרים עומדים בדרככם?
והכי חשוב איך תוכלו לשפר באופן פשוט וקל את החיסכון שלכם באופן משמעותי""",
            "date": "2024-01-02"
        },
        {
            "title": "הטבות מס",
            "text": """הטבות מס
29.10.2024

https://goola-group.com/webinars/kobi-04-12-24/?refferer_id=xxx&target=yyy""",
            "post_text": """מרבית אזרחי ישראל לא מודעים להטבות מס שמגיעות להם.
הטבות ששוות לכם המון כסף.
אז לא משנה אם אתם עצמאיים או שכירים או אפילו פנסיונרים, יש הטבות מס שתופתעו כמה הם שווים לכם והופכים את החיסכון במסלולים אלו לכדאיים במיוחד.""",
            "date": "2024-01-03"
        },
        {
            "title": "תכנית עבודה שנתית 2025",
            "text": """תכנית עבודה שנתית 2025
29.10.2024

https://goola-group.com/webinars/sarit-18-12-24/?refferer_id=xxx&target=yyy""",
            "post_text": """איך תהפכו את שנת 2025 להכי מוצלחת שאפשר?
תוכנית עבודה זה סוד ההצלחה. 
יש תוכנית – יש כיוון
יש תוכנית – יודעים מה לעשות.
אבל איך מכינים תוכנית עבודה? 
אנחנו כאן בשבילכם כדי להסביר לכם את העקרונות לכתיבת תוכנית עבודה אפקטיבית.""",
            "date": "2024-01-04"
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