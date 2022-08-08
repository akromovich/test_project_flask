from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///big.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Articles(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    text = db.Column(db.String(300),nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/projects')
def projects():
    articles = Articles.query.order_by(Articles.date.desc()).all()
    return render_template('projects.html',articles=articles)

@app.route('/projects/<int:id>')
def post_detail(id):
    article = Articles.query.get(id)
    return render_template('post_article.html',article=article)

@app.route('/projects/<int:id>/del')
def post_del(id):
    article = Articles.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/projects')
    except:
        return 'При удалении статьи произошла ошибка'

@app.route('/create_article',methods = ['POST','GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        articles = Articles(title= title,text=text)
        try:
            db.session.add(articles)
            db.session.commit()
            return redirect('/projects')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template('create_article.html')

@app.route('/projects/<int:id>/update',methods = ['POST','GET'])
def post_update(id):
    article = Articles.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/projects')
        except:
            return "При обновлении статьи произошла ошибка"
    else:
        return render_template('post_update.html',article=article)


if __name__ == '__main__':
    app.run(debug=True)
