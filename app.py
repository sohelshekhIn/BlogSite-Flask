from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import json

with open("config.json","r") as fp:
    params = json.load(fp)["params"]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
db = SQLAlchemy(app)


class Contact(db.Model):
    '''
    MySQL Database Contacts Table Refferal
    '''
    sr_no = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class Posts(db.Model):
    '''
    MySQL Database Posts Table Refferal
    '''
    sr_no = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(21), nullable=False)
    post_content = db.Column(db.String(120), nullable=False)
    post_date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(12), nullable=True)




@app.route('/')
@app.route('/index')
def index():
    posts = Posts.query.filter_by().all()
    return render_template("index.html", posts=posts) 


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if(request.method == 'POST'):
        name  = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, phone_no=phone, email=email, msg=message, date=datetime.datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html")

@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html", post=post)  


@app.route("/about")
def about():
    return render_template("about.html")


app.run(debug=True)
