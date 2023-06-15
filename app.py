from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20))
    acquisition_date = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String(20))
    university_item_number = db.Column(db.String(20))
    budget = db.Column(db.String(20))

# /はGET,POSTリクエストを受け取る
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()   
         # templatesフォルダ内のindex.htmlを表示する(返す?)
        return render_template('index.html', posts=posts)

    else:
        id = request.form.get('id')
        object = request.form.get('object')
        acquisition_date = request.form.get('acquisition_date')
        
        acquisition_date = datetime.strptime(acquisition_date, '%Y-%m-%d')

        username = request.form.get('username')
        place = request.form.get('place')
        university_item_number1 = request.form.get('university_item_number1')
        university_item_number2 = request.form.get('university_item_number2')
        university_item_number = str(university_item_number1)+"-"+str(university_item_number2)
        budget = request.form.get('budget')

        new_post = Post(id=id, object=object, acquisition_date=acquisition_date, username=username, place=place, university_item_number=university_item_number, budget=budget)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

# 物品を追加する
@app.route('/create')
def create():
    return render_template('create.html')

# 物品を削除する
@app.route('/delete/<int:id>')
def delete(id):
    # データベースに問い合わせて、与えられたidを持つpostを取得
    post = Post.query.get(id)
    # postオブジェクトの削除
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# 物品を編集する
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.id = request.form.get('id')
        post.object = request.form.get('object')
        acquisition_date = request.form.get('acquisition_date')
        
        post.acquisition_date = datetime.strptime(acquisition_date, '%Y-%m-%d')

        post.username = request.form.get('username')
        post.place = request.form.get('place')
        university_item_number1 = request.form.get('university_item_number1')
        university_item_number2 = request.form.get('university_item_number2')
        post.university_item_number = str(university_item_number1)+"-"+str(university_item_number2)
        post.budget = request.form.get('budget')

        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)