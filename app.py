from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# מודל עבור סוכנים
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    referral_id = db.Column(db.String(20), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "שם פרטי": self.first_name,
            "שם משפחה": self.last_name,
            "מספר מפנה": self.referral_id
        }

# מודלים למסד הנתונים
class SavedLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    post_text = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class GeneralText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# יצירת מסד הנתונים
with app.app_context():
    db.create_all()

# רשימת סוכנים התחלתית
initial_agents = [
    {"שם פרטי": "חלי", "שם משפחה": "דיין", "מספר מפנה": "2195"},
    {"שם פרטי": "ויקטור אביחי", "שם משפחה": "פלד", "מספר מפנה": "2421"},
    {"שם פרטי": "אלעד", "שם משפחה": "דיין", "מספר מפנה": "2192"},
    {"שם פרטי": "שמעון", "שם משפחה": "ברון", "מספר מפנה": "2060"},
    {"שם פרטי": "עמית", "שם משפחה": "ניסל", "מספר מפנה": ""},
    {"שם פרטי": "שירן", "שם משפחה": "סגיר", "מספר מפנה": "2420"},
    {"שם פרטי": "יוסי", "שם משפחה": "לוי", "מספר מפנה": "2623"},
    {"שם פרטי": "אורן", "שם משפחה": "שוקרון", "מספר מפנה": "2214"},
    {"שם פרטי": "גיא", "שם משפחה": "מרציאנו", "מספר מפנה": "2809"},
    {"שם פרטי": "שי", "שם משפחה": "וינברג", "מספר מפנה": "2487"},
    {"שם פרטי": "מאיר", "שם משפחה": "טולדנו", "מספר מפנה": "2202"},
    {"שם פרטי": "דודו", "שם משפחה": "גמרסני", "מספר מפנה": "2778"},
    {"שם פרטי": "שריה", "שם משפחה": "אשר", "מספר מפנה": "2775"},
    {"שם פרטי": "עידו", "שם משפחה": "כהן", "מספר מפנה": "1957"},
    {"שם פרטי": "איתי", "שם משפחה": "גילרן", "מספר מפנה": "2196"},
    {"שם פרטי": "דניאל", "שם משפחה": "שימונוב", "מספר מפנה": "1721"},
    {"שם פרטי": "אורי", "שם משפחה": "זהבי", "מספר מפנה": "2197"},
    {"שם פרטי": "צור", "שם משפחה": "גושן", "מספר מפנה": "1923"},
    {"שם פרטי": "ליאור", "שם משפחה": "בן טוב", "מספר מפנה": "1210"},
    {"שם פרטי": "גל", "שם משפחה": "דנגור", "מספר מפנה": "1693"},
    {"שם פרטי": "זאב", "שם משפחה": "סויבל", "מספר מפנה": "2771"},
    {"שם פרטי": "לירן", "שם משפחה": "אלרם", "מספר מפנה": "1709"},
    {"שם פרטי": "עופר", "שם משפחה": "כוכבי", "מספר מפנה": "1703"},
    {"שם פרטי": "אליאור", "שם משפחה": "זמיר", "מספר מפנה": "2777"},
    {"שם פרטי": "תמיר", "שם משפחה": "זיו", "מספר מפנה": "2128"},
    {"שם פרטי": "ענב", "שם משפחה": "שרון", "מספר מפנה": "1793"},
    {"שם פרטי": "מרוה", "שם משפחה": "אלברט", "מספר מפנה": "2806"},
    {"שם פרטי": "איתי", "שם משפחה": "ישראל", "מספר מפנה": ""},
    {"שם פרטי": "שחר", "שם משפחה": "רייף", "מספר מפנה": "2359"},
    {"שם פרטי": "אנדרי", "שם משפחה": "קונובלוב", "מספר מפנה": "2358"},
    {"שם פרטי": "ערן", "שם משפחה": "כהן", "מספר מפנה": "2747"},
    {"שם פרטי": "חגי", "שם משפחה": "רון", "מספר מפנה": "2615"},
    {"שם פרטי": "יאנה", "שם משפחה": "שרוני", "מספר מפנה": "2746"},
    {"שם פרטי": "יונתן", "שם משפחה": "שרעבי", "מספר מפנה": "1898"},
    {"שם פרטי": "לירון", "שם משפחה": "אלעזר", "מספר מפנה": "1183"},
    {"שם פרטי": "קובי", "שם משפחה": "דהאן", "מספר מפנה": "264"},
    {"שם פרטי": "שי", "שם משפחה": "נגר", "מספר מפנה": "2444"},
    {"שם פרטי": "כפיר", "שם משפחה": "קרני", "מספר מפנה": "1712"},
    {"שם פרטי": "ארז", "שם משפחה": "קראוס", "מספר מפנה": "1745"},
    {"שם פרטי": "יאיר", "שם משפחה": "סולומון", "מספר מפנה": "2283"},
    {"שם פרטי": "בנצי", "שם משפחה": "שיין", "מספר מפנה": "2422"},
    {"שם פרטי": "אריאל", "שם משפחה": "אוחיון", "מספר מפנה": "2720"},
    {"שם פרטי": "ניב", "שם משפחה": "מרקמן", "מספר מפנה": "2727"},
    {"שם פרטי": "עידו", "שם משפחה": "נוימן", "מספר מפנה": "2397"},
    {"שם פרטי": "דימה", "שם משפחה": "בוצ'וקי", "מספר מפנה": "2673"},
    {"שם פרטי": "אילן", "שם משפחה": "עזרא", "מספר מפנה": "2672"},
    {"שם פרטי": "אלי", "שם משפחה": "נדיב", "מספר מפנה": "2671"},
    {"שם פרטי": "בועז", "שם משפחה": "חן", "מספר מפנה": "2670"},
    {"שם פרטי": "אריאל", "שם משפחה": "כפיר", "מספר מפנה": "2669"},
    {"שם פרטי": "שמעון", "שם משפחה": "רוזנפלד", "מספר מפנה": "2668"},
    {"שם פרטי": "נתן", "שם משפחה": "פרידמן", "מספר מפנה": "2808"},
    {"שם פרטי": "מירב", "שם משפחה": "לוי ליבוביץ", "מספר מפנה": "1032"},
    {"שם פרטי": "אלידע", "שם משפחה": "פרינס", "מספר מפנה": "578"},
    {"שם פרטי": "אבי", "שם משפחה": "בירהון", "מספר מפנה": "2723"},
    {"שם פרטי": "יגיל", "שם משפחה": "צבעוני", "מספר מפנה": "2802"},
    {"שם פרטי": "נטליה", "שם משפחה": "מיידן", "מספר מפנה": "2805"},
    {"שם פרטי": "עמוס", "שם משפחה": "חלפון", "מס��ר מפנה": "2807"}
]

# הוספת ייבוא נדרש
import json
import os
from datetime import datetime

# הגדרת קבצי השמירה
AGENTS_FILE = 'data/agents.json'
SAVED_LINKS_FILE = 'data/saved_links.json'
GENERAL_TEXTS_FILE = 'data/general_texts.json'
TEMPLATES_FILE = 'data/templates.json'

# יצירת תיקיית data אם לא קיימת
os.makedirs('data', exist_ok=True)

def load_json_file(filename, default_value):
    """טעינת קובץ JSON עם ערך ברירת מחדל"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return default_value

def save_json_file(filename, data):
    """שמירת נתונים לקובץ JSON"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

# טעינת נתונים בהפעלת השרת
initial_agents = load_json_file(AGENTS_FILE, initial_agents)  # משתמש ברשימת הסוכנים הקיימת כברירת מחדל
saved_links = load_json_file(SAVED_LINKS_FILE, {})
general_texts = load_json_file(GENERAL_TEXTS_FILE, [])
templates = load_json_file(TEMPLATES_FILE, {})

@app.route('/', methods=['GET'])
def index():
    # טעינת כל הנתונים מהקבצים
    saved_links = load_json_file(SAVED_LINKS_FILE, {})
    general_texts = load_json_file(GENERAL_TEXTS_FILE, [])
    templates = load_json_file(TEMPLATES_FILE, {})
    
    return render_template('index.html', 
                         agents=initial_agents,
                         saved_links=saved_links,
                         general_texts=general_texts,
                         templates=templates)

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
        save_json_file(AGENTS_FILE, initial_agents)
        
        return jsonify({
            "message": "Agent added successfully",
            "agent": new_agent
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/generate_link', methods=['POST'])
def generate_link():
    agent_id = request.form['agent']
    original_link = request.form['link']
    free_text = request.form.get('free_text', '')
    
    agent = next((a for a in initial_agents if a['מספר מפנה'] == agent_id), None)
    
    if agent:
        custom_link = create_custom_link(original_link, agent['מספר מפנה'])
        if free_text:
            full_text = f"{free_text}\n\n{custom_link}"
        else:
            full_text = custom_link
        
        image_url, title, description = get_link_preview(original_link)
        
        result = {
            'custom_link': custom_link,
            'full_text': full_text,
            'image_url': image_url,
            'title': title,
            'description': description
        }
        return jsonify(result)
    return jsonify({'error': 'Agent not found'}), 400

def create_custom_link(original_link, agent_id):
    parsed_url = urlparse(original_link)
    query_params = parse_qs(parsed_url.query)
    
    query_params['refferer_id'] = [agent_id]
    query_params['target'] = [agent_id]
    
    new_query = urlencode(query_params, doseq=True)
    return parsed_url._replace(query=new_query).geturl()

def get_link_preview(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        image_url = soup.find('meta', property='og:image')
        image_url = image_url['content'] if image_url else ''
        
        title = soup.find('meta', property='og:title')
        title = title['content'] if title else ''
        
        description = soup.find('meta', property='og:description')
        description = description['content'] if description else ''
        
        return image_url, title, description
    except:
        return '', '', ''

@app.route('/api/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    try:
        global initial_agents
        initial_agents = [agent for agent in initial_agents if agent['מספר מפנה'] != agent_id]
        save_json_file(AGENTS_FILE, initial_agents)
        
        # מחיקת הקישורים השמורים של הסוכן
        if agent_id in saved_links:
            del saved_links[agent_id]
            save_json_file(SAVED_LINKS_FILE, saved_links)
            
        return jsonify({"message": "Agent deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/saved-links/<agent_id>', methods=['GET', 'POST'])
def handle_saved_links(agent_id):
    if request.method == 'POST':
        data = request.json
        new_link = SavedLink(
            agent_id=agent_id,
            title=data.get('title'),
            text=data.get('text'),
            post_text=data.get('postText')
        )
        db.session.add(new_link)
        db.session.commit()
        return jsonify({"message": "Link saved successfully"})
    
    # שליפת כל הקישורים של הסוכן
    links = SavedLink.query.filter_by(agent_id=agent_id).all()
    return jsonify([{
        'title': link.title,
        'text': link.text,
        'postText': link.post_text,
        'date': link.date_created.strftime('%Y-%m-%d %H:%M:%S')
    } for link in links])

@app.route('/api/general-texts', methods=['GET', 'POST'])
def handle_general_texts():
    if request.method == 'POST':
        data = request.json
        new_text = GeneralText(
            title=data.get('title'),
            content=data.get('content')
        )
        db.session.add(new_text)
        db.session.commit()
        return jsonify({"message": "Text saved successfully"})
    
    # שליפת כל הטקסטים הכלליים
    texts = GeneralText.query.all()
    return jsonify([{
        'title': text.title,
        'content': text.content,
        'date': text.date_created.strftime('%Y-%m-%d %H:%M:%S')
    } for text in texts])

@app.route('/api/templates', methods=['GET', 'POST'])
def handle_templates():
    global templates
    
    if request.method == 'POST':
        data = request.json
        templates[data['id']] = data['content']
        save_json_file(TEMPLATES_FILE, templates)
        return jsonify({"message": "Template saved successfully"})
    
    return jsonify(templates)

# הוספת קוד לאתחול מסד הנתונים
def init_db():
    with app.app_context():
        # יצירת כל הטבלאות
        db.create_all()
        
        # בדיקה אם יש כבר סוכנים במערכת
        if not Agent.query.first():
            # הוספת הסוכנים ההתחלתיים
            for agent_data in initial_agents:
                agent = Agent(
                    first_name=agent_data["שם פרטי"],
                    last_name=agent_data["שם משפחה"],
                    referral_id=agent_data["מספר מפנה"]
                )
                db.session.add(agent)
        
        # הוספת דוגמאות לקישורים שמורים
        if not SavedLink.query.first():
            example_links = [
                {
                    "agent_id": "2195",  # חלי דיין
                    "title": "וובינר פנסיה",
                    "text": "🎯 הזמנה לוובינר: תכנון פנסיוני חכם\n\nמה נלמד בוובינר?\n✅ איך לבחור את הפנסיה הנכונה\n✅ טיפים לחיסכון בדמי ניהול",
                    "post_text": "טקסט נוסף לפוסט"
                },
                {
                    "agent_id": "2421",  # ויקטור אביחי פלד
                    "title": "פגישת ייעוץ",
                    "text": "💰 הזמנה לפגישת ייעוץ אישית\n\nבואו נבנה יחד תכנית פיננסית מותאמת אישית",
                    "post_text": ""
                }
            ]
            
            for link_data in example_links:
                link = SavedLink(
                    agent_id=link_data["agent_id"],
                    title=link_data["title"],
                    text=link_data["text"],
                    post_text=link_data["post_text"]
                )
                db.session.add(link)
        
        # הוספת דוגמאות לטקסטים כלליים
        if not GeneralText.query.first():
            example_texts = [
                {
                    "title": "ברכת יום הולדת",
                    "content": "🎉 מזל טוב!\nמאחלים לך יום הולדת שמח ומלא באושר ושמחה!"
                },
                {
                    "title": "הזמנה לפגישה",
                    "content": "👋 היי!\nאשמח להיפגש איתך לפגישת ייעוץ אישית ללא עלות."
                }
            ]
            
            for text_data in example_texts:
                text = GeneralText(
                    title=text_data["title"],
                    content=text_data["content"]
                )
                db.session.add(text)
        
        # שמירת כל השינויים
        db.session.commit()

# הפעלת אתחול מסד הנתונים
init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)