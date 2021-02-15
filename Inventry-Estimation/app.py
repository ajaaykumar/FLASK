from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user1:test123@localhost:5432/mydb'
db = SQLAlchemy(app)


class AddressBook(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity


@app.route('/home')
def homepage():
    db.create_all()
    return render_template('base.html')


@app.route('/show_all')
def show_all():
    return render_template('show_all.html', result=AddressBook.query.all())


@app.route('/new_addr', methods=['POST', 'GET'])
def new_addr():
    if request.method == 'POST':
        address = AddressBook(request.form.get('Product'), request.form.get('pnumber'))
        db.session.add(address)
        db.session.commit()
    return render_template('index.html', result=AddressBook.query.all())


@app.route('/update', methods=['POST', 'GET'])
def update_addr():
    if request.method == 'POST':
        print("Inside POST")
        try:
            id = request.form['id']
            Details = AddressBook.query.filter_by(id=id).first()
            Details.name = request.form.get('Product')
            Details.quantity = request.form.get('pnumber')
            db.session.commit()
        except:
            msg = "error during update operation"
            print(msg)
    return render_template('update.html', Details = AddressBook.query.all())


if __name__ == '__main__':
    app.run(debug=True)
