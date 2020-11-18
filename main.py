from flask import Flask, render_template, request, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.secret_key = "euroavia"
db = SQLAlchemy(app)


class Messages(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column(db.String(20))
    text = db.Column(db.String(280))

    def __init__(self, user, text):
        self.user = user
        self.text = text


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form["nickname"]
        session["user"] = user
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/", methods=["POST", "GET"])
def home():
    if "user" in session:
        all_texts = Messages.query.all()

        user = session["user"]

        if request.method == "POST":
            msg_text = request.form["message"]
            if msg_text != "":
                new_text = Messages(user, msg_text)
                db.session.add(new_text)
                db.session.commit()

                return redirect(url_for("home"))

        return render_template("home.html", user=user, messages=all_texts)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    app.run(debug=True)
