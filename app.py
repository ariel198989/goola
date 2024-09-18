from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse, parse_qs, urlencode

app = Flask(__name__)

# רשימה מעודכנת של סוכנים
agents = [
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
    {"שם פרטי": "עמוס", "שם משפחה": "חלפון", "מספר מפנה": "2807"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', agents=agents)

@app.route('/generate_link', methods=['POST'])
def generate_link():
    agent_id = request.form['agent']
    original_link = request.form['link']
    
    agent = next((a for a in agents if a['מספר מפנה'] == agent_id), None)
    if agent:
        custom_link = create_custom_link(original_link, agent['מספר מפנה'])
        return jsonify({'custom_link': custom_link})
    return jsonify({'error': 'Agent not found'}), 400

def create_custom_link(original_link, agent_id):
    parsed_url = urlparse(original_link)
    query_params = parse_qs(parsed_url.query)
    
    query_params['refferer_id'] = [agent_id]
    query_params['target'] = [agent_id]
    
    new_query = urlencode(query_params, doseq=True)
    return parsed_url._replace(query=new_query).geturl()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)