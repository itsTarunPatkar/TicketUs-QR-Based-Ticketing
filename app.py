from flask import Flask, redirect, render_template as render, session, url_for
from flask_sqlalchemy import SQLAlchemy, request
from sqlalchemy import true
from flask_qrcode import QRcode
import firebase_admin
import requests
import json
from firebase_admin import firestore, auth
import qrcode
import socket


# ipaddress = socket.gethostbyname(socket.gethostname())
ipaddress = "localhost"
cred_obj = firebase_admin.credentials.Certificate('./key.json')
default_app = firebase_admin.initialize_app(cred_obj)
firestore_client = firestore.client()

FB_WEB_API_KEY = "AIzaSyALhKKF-Tgh90KJQbtwzKI8Xbac-SvsNCQ"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/TicketUS'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
QRcode(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(55), unique=True, nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(16), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)

@app.route('/feedback', methods=["POST"])
def feedback():
    email = request.form.get('email')
    message = request.form.get('message')
    entry = Feedback(email=email, message=message)
    db.session.add(entry)
    db.session.commit()
    return redirect('/')


def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(rest_api_url,
                      params={"key": FB_WEB_API_KEY},
                      data=payload)

    return r.json()

@app.route("/", methods=['GET', 'POST'])
def home():
    print(session.keys())
    if request.method == 'POST':
        data = dict(request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        if email is None or password is None:
            session["error"] = True
            return redirect('/#register')
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            token = sign_in_with_email_and_password(email, password)
            session["userId"] = token["localId"]
            session["user"] = data["name"]
            auth.update_user(session["userId"], display_name = data["name"], phone_number=data["phone"])
            return redirect('/')
        except Exception as e:
            print(e)
            session["error"] = True
            return redirect('/#register')
    """  # dic = dict(request.form)
        # print(dic)
        # # name = request.form.get('name')
        # # email = request.form.get('email')
        # # phone = request.form.get('phone')
        # # password = request.form.get('password')
        # # condPassword= request.form.get('confPassword')
        # if dic["password"] == dic["confPassword"]: 
        #     firestore_client.collection("users").add(dic)
        # #     entry = Users(name=name, phone_no=phone, email=email, password=password)
        #     # db.session.add(entry)
        #     # db.session.commit()
        #     return redirect(url_for('login'))
        # else: 
        #     session["error"] = True
        #     return redirect('/#register') """
    session.pop('error1', None)
    return render("home.html")

@app.route("/logout")
def logout():
    session.pop('userId',None)
    session.pop('user',None)
    return redirect('/')

@app.route("/contact")
def contact():
    return render("contact.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session and session['user'] is not None:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 
        if username is None or password is None:
            session["error"] = True
            print("error1")
            return redirect('/login')
        try:
            token = sign_in_with_email_and_password(username, password)
            print(token.get("localId"))
            session.pop('user',None)
            session["userId"]=token.get("localId")
            session["user"]=token.get("displayName")
            print(session)
            return redirect('/')
        except Exception as e:
            session["error"] = True
            print("error2", e)
            return redirect('/login')
        # username = request.form.get('username')
        # password = request.form.get('password') 
        # data = Users.query.filter_by(email=username).first()
        # dbPassword = data.password
        # user = data.name.split()[0]
        # print(f'{username = } {password = } {user = }')
        # if password == dbPassword:
        #     session.pop('user',None)
        #     session["user"] = user
        #     return redirect('/')
        # else:
        #     session["error1"] = True
        #     return redirect('/login')
    session.pop('error', None)
    return render("login.html")

@app.route("/form")
def formsss():
    if 'user' not in session:
        return redirect('/login')

    urls = {"Tajmahal":"images/tajmahal (1).jpg", 
            "Qutub Minar":"images/rajeev-pal-I3gZE5pfVoY-unsplash.jpg", 
            "Khajuraho":"images/praniket-desai-5yaZgm9bIh8-unsplash.jpg", 
            "Gwalior Fort":"images/yash-kiran-Ii4-mpa_g3Y-unsplash.jpg", 
            "Sanchi Stupa":"images/deepanshu-arora-jXzX1Kdh6G0-unsplash.jpg", 
            "Rani Kamlapati Fort":"images/bhaumik-shrivastava-T0A4H155SxE-unsplash.jpg"}
    return render("visitorForm.html", img_url = urls[request.args.get('location')])

@app.route("/monuments")
def monument():
    return render("monuments.html",  data = [
            {"img_url":"images/tajmahal.jpg", "name":"Tajmahal", "desc": "The Taj Mahal is a designated UNESCO World Heritage monument and the absolute pinnacle of Mughal architecture. The Taj Mahal is a designated UNESCO World Heritage monument and the absolute pinnacle of Mughal architecture.", "price":45, "location": " Dharmapuri, Forest Colony, Tajganj, Agra, Uttar Pradesh 282001"},
            {"img_url":"images/rajeev-pal-I3gZE5pfVoY-unsplash.jpg", "name":"Qutub Minar", "desc": "As you enter, the glorified plaques greet you giving you the slice of history and what Qutub Minar stands for. But Qutub Minar is many things for many people. ", "price":35, "location": " Seth Sarai, Mehrauli, New Delhi, Delhi 110030"},
            {"img_url":"images/praniket-desai-5yaZgm9bIh8-unsplash.jpg", "name":"Khajuraho", "desc": "Khajuraho, the ancient Kharjjura-vahaka represent today a distinct pattern of art and temple architecture of its own, reminding one of the rich and creative period it witnessed during .....", "price":35, "location": " Chattarpur district in Madhya Pradesh. The Khajuraho Temple address is Khajuraho, Madhya Pradesh 471606."},
            {"img_url":"images/yash-kiran-Ii4-mpa_g3Y-unsplash.jpg", "name":"Gwalior Fort", "desc": "Legend states that the Gwalior Fort was built by a local king in honour of the saint who cured ......", "price":20, "location": "  VW2C+QJQ, Khajuraho Airport Area, Khajuraho, Madhya Pradesh 471606"},
            {"img_url":"images/deepanshu-arora-jXzX1Kdh6G0-unsplash.jpg", "name":"Sanchi Stupa", "desc": "Unique in India because of its age and quality, the Buddhist stupas and monasteries at Sanchi...", "price":35, "location": " Sanchi Town, Madhya Pradesh."},
            {"img_url":"images/bhaumik-shrivastava-T0A4H155SxE-unsplash.jpg", "name":"Rani Kamlapati Fort", "desc": "Rani Kamlapati Palace is the commemoration of the glorious past of Bhopal.", "price":20, "location": "Bhopal, Madhya Pradesh"},
        ])

@app.route('/data', methods=["GET", "POST"])
def submit():
    # i = 0
    # data = []
    # temp = {}
    # for k, l in dic.items():
    #     print(f'{k = }, {l = }')
    #     if k[-1] != str(i):
    #         print(f'{temp = }')
    #         data.append(temp)
    #         temp = {}
    #         i+=1
    #     temp[k[:-2]] = l
    # else:
    #     data.append(temp)
    #     temp = {}


    dic = dict(request.form)
    _, ref_id = firestore_client.collection(u'visitordata').add(dic)
    print(ref_id.id)
    qrString = f'{ipaddress}:3300/userData?id={ref_id.id}'
    img = qrcode.make(qrString)
    img.save('./static/images/qr.png')
    

    # print(f'{data = }\n {dic = }')
    return render('afterFormQr.html', user = {"name": dic["name_0"]})


@app.route("/userData")
def getRequest():
    id = request.args.get('id')
    data = firestore_client.collection(u'visitordata').document(id.strip()).get()
    if data.exists:
        i = 0
        data2 = []
        temp = {}
        dic = data.to_dict()
        print(f'{dic = }')
        for key, values in dic.items():
            print(f'{key = }, {values = }')
            if str(len(data2)) == key[-1]: data2.append({})
            data2[int(key[-1])][key[:-2]]= values
            
        print(f'{data2 = }')
        return render('userData.html',collection=data2)
        
    else:
        print(u'No such document!', id, data.to_dict())
    return redirect('/')



@app.route("/templesCateg")
def templesCateg():
    return render("templesCateg.html")

@app.route("/wildLifeCateg")
def wildLifeCateg():
    return render("wildLifeCateg.html",  data = [
            {"img_url":"images/dumna.jpg", "name":"Dumna Nature Reserve Park", "desc": "Dumna Nature Reserve Park happens to be a place in Jabalpur, which is home to a wide range of flora and fauna. The nature reserve is spread over an area of 1058 hectares near Khandari Dam, which is situated at a distance of 10 km from Jabalpur.", "price":"20 Rs", "location": " Dumna Nature Reserve Park is located at Airport Road, near IIITDM, Jabalpur, Madhya Pradesh.", "city": 'Jabalpur'},
            {"img_url":"images/National_Chambal.jpg", "name":"National Chambal Wildlife Sanctuary", "desc": "Of all the wildlife sanctuaries in Madhya Pradesh, National Chambal is possibly the finest! Straddling the tricky-state area of UP, Madhya Pradesh, and Rajasthan, the sanctuary harbors a rich plethora of fauna, endangered and otherwise. ", "price":"Safari cost Must be there." , "location": " Covering Uttar Pradesh, Rajasthan, and Madhya Pradesh"},
            {"img_url":"images/Orchha_wild.jpg", "name":"Orchha Wildlife Sanctuary", "desc": "Perched along the banks of the river Betwa, Orchha Sanctuary is possibly the most quaint yet scenic wildlife sanctuary in Madhya Pradesh. While wildlife spotting might not be very prominent here, activities like rafting, boating, camping, and trekking more than make up for it!", "price":"Free", "location": " Orchha, Madhya Pradesh, 494661"},
            {"img_url":"images/pachmari.jpg", "name":"Pachmarhi Wildlife Sanctuary", "desc": "A beautiful sanctuary lying in the folds of the Satpura Range of Madhya Pradesh, Pachmarhi earned the designation of a 'biosphere reserve' by UNESCO in 2009. Home of many exquisite species of wildlife, and a herd of tribal folks, the beauty of the reserve is amplified by a line of ancient caves it harbours, rendering it archaeologically significant!", "price":20, "location": " Pachmarhi, Madhya Pradesh, du"},
            
        ])
  
if __name__ == "__main__":
  app.run("localhost", 3300, debug=True)
    