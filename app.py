import os
from flask import Flask, render_template, request,url_for
from flask.helpers import send_from_directory
import requests
# from urllib.parse import quote
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class History(db.Model):
    english = db.Column(db.String(80), unique=True,primary_key=True, nullable=False)
    hindi = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User is {self.english}"



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def translate():
    english = ''
    if request.method == 'POST':
        english = request.form["English Text"]
    url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"

    querystring = {"q":english,"langpair":"EN|HI","de":"a@b.c","onlyprivate":"0","mt":"1"}

    headers = {
    'x-rapidapi-key': "a56087bbe6msh7ea9fcbe14c5252p13739fjsne8785f6e7e85",
    'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    dict = json.loads(response.text)
    hindi = dict['responseData']['translatedText']
    history = History(english =english, hindi = hindi)
    db.session.add(history)
    db.session.commit()
    return render_template('index.html', hindi = hindi )


@app.route('/history', methods = ['GET', 'POST'])
def history():
    if request.method == 'POST':
        english = request.form["serial"]
        toDel = History.query.filter_by(english = english).first()
        db.session.delete(toDel)
        db.session.commit()
    records = History.query.all()
    return render_template('history.html', records = records)

@app.route('/deleteAll', methods = ['GET', 'POST'])
def deleteAll():
    if request.method == 'POST':
        translations = History.query.all()
        for translation in translations:
            db.session.delete(translation)
        db.session.commit()
    return render_template('history.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/x-icon')





if __name__ == '__main__':
    app.run(debug=True)
