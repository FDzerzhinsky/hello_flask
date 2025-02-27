from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder="./")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    support = db.Column(db.String(100))
    placement = db.Column(db.String(100))

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
                title=request.form.get('title'),
                first_name=request.form.get('firstName'),
                last_name=request.form.get('lastName'),
                email=request.form.get('email'),
                address=request.form.get('address'),
                support=request.form.get('support'),
                placement=request.form.get('placement'),

                intro=request.form.get ('intro', ''),
                text=request.form.get('text', ''),
                robot_type=request.form.get('category', ''),
                axes=request.form.get('subcategory1', ''),
                manufacturer=request.form.get('subcategory2', ''),
                model=request.form.get('subcategory3', '')
            )
            db.session.add(article)
            db.session.commit()
            return redirect('/articles')
        except Exception as e:
            return f"Ошибка: {str(e)}"

    robot_data = {
    "Промышленный": {
        "Количество Осей": ["4", "6"],
        "Производители": ["Estun", "REDS"],
        "Модели": {
            "Estun": ["ER3-450", "ER6-1600"],
            "REDS": ["RDS-200", "RDS-300"]
        }
    },

        "Коллаборативный": {
            "Количество Осей": ["6", "7"],
            "Производители": ["ur", "fanuc"],
            "Модели": {
                "ur": ["450", "1600"],
                "fanuc": ["200", "00"]
            }
        }
    }
    return render_template("create-article.html", data=robot_data)

@app.route('/articles')
def articles():
    all_articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("about.html", articles=all_articles)

@app.route('/articles/<int:id>')
def article_detail(id):
    article = Article.query.get(id)
    return render_template("article_detail.html", article=article)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)