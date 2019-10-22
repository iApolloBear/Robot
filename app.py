from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    md5 = db.Column(db.String(700))
    sha = db.Column(db.String(700))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, palabra):
        self.content = palabra
        self.md5 = five(palabra)
        self.sha = two(palabra)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        word_content = request.form['content']
        new_word = Word(word_content)
        try:
            db.session.add(new_word)
            db.session.commit()
            return redirect('/')
        except:
            return "There's Something Wrong"
    else:
        words = Word.query.order_by(Word.date_created).all()
    return render_template('index.html', words=words)


def five(word):
    encrypter = hashlib.md5()
    encrypter.update(word.encode('utf-8'))
    return encrypter.hexdigest()


def two(word):
    encrypter = hashlib.sha256()
    encrypter.update(word.encode('utf-8'))
    return encrypter.hexdigest()


@app.route('/delete/<int:id>')
def delete(id):
    word_to_delete = Word.query.get_or_404(id)
    try:
        db.session.delete(word_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    word = Word.query.get_or_404(id)

    if request.method == 'POST':
        word.content = request.form['content']
        word.md5 = five(word.content)
        word.sha = two(word.content)
        word.date_created = d

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', word=word)


if __name__ == "__main__":
    app.run(debug=True)

