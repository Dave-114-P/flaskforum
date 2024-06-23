
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
	pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

class Topic(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	title: Mapped[str] = mapped_column(unique=True)
	description: Mapped[str]

class Comment(db.Model):
	id: Mapped[int] = mapped_column(primary_key=True)
	text: Mapped[str] = mapped_column(unique=True)
	topicId: Mapped[str]

with app.app_context():
	db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
	if request.method == "POST":
		# add a topic
		topic = Topic(
			title=request.form["title"],
			description=request.form["description"],
		)
		db.session.add(topic)
		db.session.commit()
	
	topics = db.session.execute(db.select(Topic)).scalars()
	for topic in topics:
		print(topic.title, topic.description, topic.id)
	return render_template("index.html")

@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
	if request.method == "POST":
		# add a comment to topic
		comment = Comment(
			text=request.form["text"],
			topicId=request.form["topicId"],
		)
		db.session.add(comment)
		db.session.commit()
	return render_template("user/detail.html")

app.run(debug=True,port=5001)
