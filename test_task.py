from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import Users, db

# Подключение к базе данных
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rtf558Ur@localhost/Task'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)

# Подключение модуля LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Проверка вхождения в аккаунт
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Объявление страницы главной страницы
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    else:
        return render_template('index.html')

# Объявление страницы /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('users'))
        else:
            flash('Неправильный логин или пароль')
    return render_template('login.html')

# Объявление страницы /register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user = Users.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = Users(username=username, password=hashed_password, first_name=first_name, last_name=last_name)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('register.html')

# Объявление страницы /users
@app.route('/users', methods=['GET'])
def users():
    if current_user.is_authenticated:
        users_list = Users.query.all()
        return render_template('users.html', user=current_user, users_list=users_list)
    else:
        return redirect(url_for('login'))

# Функция выхода из аккаунта
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Объявление страницы /add
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        new_item = Users(username=username, password=generate_password_hash(password), first_name=first_name,
                         last_name=last_name)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/users')
    return render_template('add.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
