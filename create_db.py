from flask import Flask
from models import Users, db
from werkzeug.security import generate_password_hash
from config import user, password, db_name

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@localhost/{db_name}'
db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Создание пользователей
        user1 = Users(first_name='Robert', last_name='Vasquez', username='VasROB',
                      password=generate_password_hash('{YqT=N0<1i'))
        user2 = Users(first_name='James', last_name='Waters', username='JAwater',
                      password=generate_password_hash('9^X+le\!yG'))
        user3 = Users(first_name='Michael', last_name='Santos', username='Misant',
                      password=generate_password_hash('AS?*:7QWr0'))
        user4 = Users(first_name='Fred', last_name='Harris', username='Harred',
                      password=generate_password_hash('YD*tZ&%iv7'))
        user5 = Users(first_name='Michael', last_name='Mitchell', username='MitaeL',
                      password=generate_password_hash('3s_KK0HchiA'))
        user6 = Users(first_name='Mark', last_name='Barnett', username='Bar_Mar',
                      password=generate_password_hash('8J0e^ZuLZ*k'))
        user7 = Users(first_name='Christopher', last_name='Barton', username='CH^ton',
                      password=generate_password_hash('QC96r\9)PLz'))
        user8 = Users(first_name='Ernest', last_name='Carroll', username='EroLL',
                      password=generate_password_hash('<f\BMgba3o['))
        user9 = Users(first_name='Jerry', last_name='Vega', username='VegaS',
                      password=generate_password_hash('Qry/5242UH&'))
        user10 = Users(first_name='Brian', last_name='Kelley', username='KelBR',
                       password=generate_password_hash('2ojn:>0Xalp'))

        db.session.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9, user10])
        db.session.commit()
