from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import os


with open("config.json", 'r') as c:
    params = json.load(c)['params']

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:test123@localhost:5432/mydb'
db = SQLAlchemy(app)


class Details(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    mobile = db.Column(db.String(12))
    email = db.Column(db.String(100))
    imagename = db.Column(db.String(100))

    def __init__(self, name, mobile, email, imagename):
        self.name = name
        self.mobile = mobile
        self.email = email
        self.imagename = imagename


@app.route('/')
def homepage():
    db.create_all()
    return render_template('upload.html')


f = ''
@app.route('/uploader', methods=['POST', 'GET'])
def uploader():
    global f
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        # image uploader
        address = Details(request.form.get('name'), request.form.get('mobile'), request.form.get('email'), f.filename)
        db.session.add(address)
        db.session.commit()

        return render_template('Details.html', result=Details.query.all(), filename=f)
    return render_template('Details.html', result=Details.query.all(), filename=f)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)






