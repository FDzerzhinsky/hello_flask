from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    robot_type = db.Column(db.String(50))
    axes = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))

    def __repr__(self):
        return f'<Article {self.id}>'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        try:
            article = Article(
                title=request.form['title'],
                intro=request.form['intro'],
                text=request.form['text'],
                robot_type=request.form['category'],
                axes=request.form['subcategory1'],
                manufacturer=request.form['subcategory2'],
                model=request.form['subcategory3']
            )
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Ошибка: {str(e)}"

    robot_data = {
        "Промышленный": {
            "Количество Осей": ["4", "6"],
            "Производитель": {
                "Estun": ["ER3-450", "ER6-1600"],
                "REDS": ["RDS-200", "RDS-300"]
            }
        },
        "Коллаборативный": {
            "Количество Осей": ["6", "7"],
            "Производитель": {
                "UR": ["UR3", "UR5"],
                "Fanuc": ["CR-7iB", "CR-15iB"]
            }
        }
    }
    return render_template("create-article.html", data=robot_data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)