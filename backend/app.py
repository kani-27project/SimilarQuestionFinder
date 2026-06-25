from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
CORS(
    app,
    resources={r"/*": {"origins": "*"}}
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------- USER TABLE ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# ---------------- QUESTION TABLE ----------------

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100))
    user_id = db.Column(db.Integer)


# ---------------- HOME ----------------

@app.route("/")
def home():
    return {"message": "Database Connected"}


# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    email = data["email"]
    password = generate_password_hash(data["password"])

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"message": "User already exists"}, 400

    user = User(
        email=email,
        password=password
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "Signup Successful"}


# ---------------- LOGIN ----------------

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        return {
            "message": "Login Successful",
            "user_id": user.id,
            "email": user.email
        }

    return {
        "message": "Invalid Credentials"
    }, 401


# ---------------- TEST USER ----------------

@app.route("/testsignup")
def testsignup():

    user = User(
        email="kani@gmail.com",
        password="123456"
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "Test User Added"}


# ---------------- ADD QUESTION ----------------

def get_topic(question):

    question = question.lower()

    if any(word in question for word in ["photosynthesis", "plant", "cell", "biology"]):
        return "Biology"

    if any(word in question for word in ["force", "motion", "energy", "physics"]):
        return "Physics"

    if any(word in question for word in ["equation", "algebra", "math", "geometry"]):
        return "Math"

    return "General"

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_questions(new_question):

    all_questions = Question.query.all()

    if len(all_questions) == 0:
        return []

    questions = [q.question for q in all_questions]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        questions + [new_question]
    )

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    result = []

    for i, score in enumerate(similarities):

        result.append({
            "question": questions[i],
            "topic": all_questions[i].topic,
            "similarity": round(float(score) * 100, 2)
        })

    result.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return result[:5]

@app.route("/add-question", methods=["POST"])
def add_question():

    data = request.get_json()

    question_text = data["question"]

    existing = Question.query.filter_by(
        question=question_text
    ).first()

    if existing:
        return {
            "message": "Question Already Exists",
            "topic": existing.topic
        }

    topic = get_topic(question_text)

    q = Question(
        question=question_text,
        topic=topic,
        user_id=1
    )

    db.session.add(q)
    db.session.commit()

    return {
        "message": "Question Added",
        "topic": topic
    }


# ---------------- VIEW USERS ----------------

@app.route("/users")
def users():

    all_users = User.query.all()

    result = []

    for user in all_users:
        result.append({
            "id": user.id,
            "email": user.email
        })

    return result



# ---------------- VIEW QUESTIONS ----------------

@app.route("/similar", methods=["POST"])
def similar():

    data = request.get_json()

    question = data["question"]

    results = find_similar_questions(question)

    return results

@app.route("/questions")
def questions():

    all_questions = Question.query.all()

    result = []

    for q in all_questions:
        result.append({
            "id": q.id,
            "question": q.question,
            "topic": q.topic,
            "user_id": q.user_id
        })

    return result

@app.route("/history/<int:user_id>")
def history(user_id):

    questions = Question.query.filter_by(
        user_id=user_id
    ).all()

    result = []

    for q in questions:
        result.append({
            "id": q.id,
            "question": q.question,
            "topic": q.topic
        })

    return result
# ---------------- DATABASE ----------------

with app.app_context():
    db.create_all()


# ---------------- RUN APP ----------------

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )