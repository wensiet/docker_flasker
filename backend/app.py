from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from flask import redirect
import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


def get_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(250), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def hello():
    return render_template("home.html")


@app.route('/create_article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error while adding article."
        # TODO обработать пост запрос и добавить хуету в БД
    else:
        return render_template("create-article.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detailed(id):
    article = Article.query.get(id)
    return render_template('post_detailed.html', article=article)


@app.route('/posts/delete/<int:id>')
def delete_post(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except Exception:
        return "There is no such article."


@app.route('/get-query')
def get_query():
    data = request.args.get('id')
    return '''<h2>Got data: {}</h2>'''.format(data)


if __name__ == "__main__":
    ip = '194.58.118.188'
    app.run(host=ip, port=80)  # smth
