from flask import Flask,render_template,url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

robot_data = {
    "Промышленный": {
        "Количество Осей": ["4", "6"],
        "Производитель": {
            "Estun": ["LS3-450", "G3-251S"],
            "REDS": ["HM-4035", "HS-4045"]
        }
    },
    "Коллаборативный": {
        "Количество Осей": ["4", "6"],
        "Производитель": {
            "Estun": ["IRB 1200-5/0.7", "IRB 4600-40/2.55"],
            "REDS": ["R-2000iB/165F", "CR-35iA"]
        }
    },
    "Дельта": {
        "Количество Осей": ["4", "6"],
        "Производитель": {
            "Estun": ["IRB 360-1/1130", "IRB 390 FlexPacker"],
            "REDS": ["M-3iA/6A", "DR-3iB/6H"]
        }
    }
}


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index ():
    return render_template("index.html")


@app.route('/about')
def about ():
    return render_template("about.html")

@app.route('/create-article', methods=['GET', 'POST'])
def create_article ():
    robot_type = request.form.get('robot_type', list(robot_data.keys())[0])  # Default value
    axes_options = robot_data[robot_type]["Количество Осей"]
    axes = request.form.get('axes', axes_options[0] if axes_options else '') #Default axis

    manufacturer_options = []
    manufacturer = ''
    if axes:
        manufacturer_options = list(robot_data[robot_type]["Производитель"].keys())
        manufacturer = request.form.get('manufacturer', manufacturer_options[0] if manufacturer_options else '') #Default manufacturer

    model_options = []
    model = ''
    if manufacturer:
        model_options = robot_data[robot_type]["Производитель"][manufacturer]
        model = request.form.get('model', model_options[0] if model_options else '') #Default model

    return render_template("create-article.html",
                           robot_type=robot_type,
                           robot_types=robot_data.keys(),
                           axes=axes,
                           axes_options=axes_options,
                           manufacturer=manufacturer,
                           manufacturer_options=manufacturer_options,
                           model=model,
                           model_options=model_options
                           )

if __name__ == "__main__":
    app.run(debug=True)