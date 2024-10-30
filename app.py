from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# הגדרת מסד הנתונים
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# יצירת תיקיית data אם לא קיימת
os.makedirs('data', exist_ok=True)

# מודלים למסד הנתונים
class SavedLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    post_text = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# יצירת מסד הנתונים
with app.app_context():
    db.create_all()

# הוספת קובץ נתונים קבוע
SAVED_DATA = {
    'templates': {
        'pension_webinar': """🎯 הזמנה לוובינר: "תכנון פנסיוני חכם - המפתח לעתיד כלכלי בטוח"

מה נלמד בוובינר?
✅ איך לבחור את הפנסיה הנכונה עבורכם
✅ טיפים לחיסכון משמעותי בדמי ניהול
[...]""",
        'family_webinar': """[...]""",
        # ... שאר התבניות
    },
    
    'saved_links': {
        '2195': [  # קוד סוכן
            {
                'title': 'וובינר פנסיה',
                'text': 'טקסט לדוגמה...',
                'post_text': 'טקסט נוסף...',
                'date': '2024-01-01'
            },
            # ... עוד קישורים שמורים
        ]
    },
    
    'general_texts': [
        {
            'title': 'ברכת יום הולדת',
            'content': '🎉 מזל טוב!\nמאחלים לך...',
            'date': '2024-01-01'
        },
        # ... עוד טקסטים כלליים
    ]
}

# פונקציה לטעינת הנתונים
def get_saved_data():
    return SAVED_DATA

# פונקציה להוספת קישור חדש
@app.route('/api/saved-links/<agent_id>', methods=['POST'])
def add_saved_link(agent_id):
    data = request.json
    if agent_id not in SAVED_DATA['saved_links']:
        SAVED_DATA['saved_links'][agent_id] = []
    
    SAVED_DATA['saved_links'][agent_id].append({
        'title': data['title'],
        'text': data['text'],
        'post_text': data.get('post_text', ''),
        'date': datetime.now().strftime('%Y-%m-%d')
    })
    
    return jsonify({"success": True})

@app.route('/')
def index():
    return render_template('index.html', agents=initial_agents)

if __name__ == '__main__':
    # הגדרת השרת לעבוד על הפורט הנכון
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)