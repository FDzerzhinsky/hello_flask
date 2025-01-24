from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///checkout.db'
db = SQLAlchemy(app)

class Checkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Item {self.id}'

@app.route('/')
@app.route('/home')
def index():  # put application's code here
    return render_template('index.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')
@app.route('/user/<string:name>/<int:id>')
def user(name, id):  # put application's code here
    return 'Юзер по имени ' + name + ' с id ' + str(id)

if __name__ == '__main__':
    app.run(debug=True)

