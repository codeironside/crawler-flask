import os
import random
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, send_file
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir, "database.sqlite")

db = SQLAlchemy(app)

class RandomNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    file = db.Column(db.String)
    date_time = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())
    
    @property
    def cleaned_date_time(self):
        return f"{self.date_time.day}/{self.date_time.month}/{self.date_time.year}"

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')

@app.route('/results/',methods=['GET'])
def display_results():
    results = RandomNumber.query.all()
    
    context = {
        "results":results
    }
    
    return render_template("results.html", context=context)

@app.route('/scrape/', methods=['GET','POST'])
def scrper():
    if request.method == "POST":
        """
            Call the scrapper function here
        """
        number = random.randint(0,59)
        context = {
            "result": number
        }
        new_random_number = RandomNumber(number=number, file=os.path.join(basedir, "media/hello.txt"))
        db.session.add(new_random_number)
        db.session.commit()
        return render_template("scrapper_result.html", context=context)
    return render_template("scrapper.html")

@app.route("/download/<path:file>/", methods=["GET"])
def download(file):
    return send_file(file, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #DEBUG is SET to TRUE. CHANGE FOR PROD
        app.run(port=5000,debug=True)
    