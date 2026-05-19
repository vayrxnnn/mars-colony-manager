from flask import Flask, render_template, redirect, request, jsonify
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, IntegerField, FileField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.category import Category
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data.users_resource import UsersResource, UsersListResource
from data import jobs_api
from flask import make_response
from data import users_api
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mars_secret_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    leader = IntegerField('ID руководителя команды', validators=[DataRequired()])
    worksize = IntegerField('Продолжительность работы', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    categories = StringField('Категории')
    accept = BooleanField('Работа завершена?')
    submit = SubmitField('Сохранить')


class RegisterForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    speciality = StringField('Профессия', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    city_from = StringField('Родной город', validators=[DataRequired()])
    avatar = FileField('Фото профиля')
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class DepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    chief = IntegerField('ID начальника', validators=[DataRequired()])
    members = StringField('Члены департамента', validators=[DataRequired()])
    email = StringField('Email департамента', validators=[DataRequired()])
    submit = SubmitField('Сохранить')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form, message='Такой пользователь уже есть')
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            city_from=form.city_from.data
        )

        file = form.avatar.data
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/img', filename)
            file.save(filepath)
            user.avatar = filename

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('index.html', jobs=jobs, title='Список работ')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader=form.leader.data,
            work_size=form.worksize.data,
            collaborators=form.collaborators.data,
            is_finished=form.accept.data
        )
        db_sess.add(job)

        if form.categories.data:
            categories_ids = {int(x.strip()) for x in form.categories.data.split(',') if x.strip().isdigit()}
        else:
            categories_ids = set()
        for cat_id in categories_ids:
            category = db_sess.get(Category, cat_id)
            if category:
                job.categories.append(category)

        db_sess.commit()
        db_sess.close()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           subtitle='Заполните форму для создания новой задачи', form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = AddJobForm()

    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).filter(Jobs.id == id).first()

    if not job:
        return 'Работа не найдена'

    if current_user.id != job.team_leader and current_user.id != 1:
        return 'Доступ запрещен'

    if request.method == 'GET':
        form.job.data = job.job
        form.leader.data = job.team_leader
        form.worksize.data = job.work_size
        form.collaborators.data = job.collaborators
        form.accept.data = job.is_finished
        form.categories.data = ', '.join(str(category.id) for category in job.categories)

    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.leader.data
        job.work_size = form.worksize.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.accept.data
        job.categories.clear()

        if form.categories.data:
            categories_ids = {int(x.strip()) for x in form.categories.data.split(',') if x.strip().isdigit()}
        else:
            categories_ids = set()

        for cat_id in categories_ids:
            category = db_sess.get(Category, cat_id)
            if category:
                job.categories.append(category)

        db_sess.commit()
        db_sess.close()
        return redirect('/')

    return render_template('add_job.html', title='Редактирование работы',
                           subtitle='Заполните форму для редактирования выбранной задачи', form=form)


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).filter(Jobs.id == id).first()

    if not job:
        return 'Работа не найдена'

    if current_user.id != job.team_leader and current_user.id != 1:
        return 'Доступ запрещен'

    db_sess.delete(job)
    db_sess.commit()
    db_sess.close()
    return redirect('/')


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    return render_template('departments.html',
                           departments=departments,
                           title='Департаменты')


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        department = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data
        )

        db_sess.add(department)
        db_sess.commit()
        db_sess.close()
        return redirect('/departments')

    return render_template('department_form.html',
                           title='Добавить Департамент',
                           form=form)


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()

    db_sess = db_session.create_session()
    department = db_sess.get(Department, id)

    if not department:
        return 'Департамент не найден'

    if current_user.id != department.chief and current_user.id != 1:
        return 'Доступ запрещен'

    if request.method == 'GET':
        form.title.data = department.title
        form.chief.data = department.chief
        form.members.data = department.members
        form.email.data = department.email

    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data

        db_sess.commit()
        db_sess.close()
        return redirect('/departments')

    return render_template('department_form.html',
                           title='Редактировать Департамент',
                           form=form)


@app.route('/delete_department/<int:id>')
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    department = db_sess.get(Department, id)
    if not department:
        return 'Департамент не найден'
    if current_user.id != department.chief and current_user.id != 1:
        return 'Доступ запрещен'
    db_sess.delete(department)
    db_sess.commit()
    db_sess.close()
    return redirect('/departments')


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)

    if not user:
        return 'Пользователь не найден'
    city = user.city_from
    if not city:
        return 'У пользователя не указан родной город'

    full_name = f"{user.surname} {user.name}"
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=8013b162-6b42-4997-9691-77b7074026e0&geocode={city}&format=json"

    try:
        geo_response = requests.get(geocoder_request, timeout=5)
        if geo_response.status_code != 200:
            return 'Ошибка геокодера'

        json_response = geo_response.json()
        features = json_response["response"]["GeoObjectCollection"]["featureMember"]

        if not features:
            return f'Город "{city}" не найден на карте'

        pos = features[0]["GeoObject"]["Point"]["pos"]

    except Exception:
        return 'Не удалось получить данные о координатах'

    return render_template(
        'users_show.html',
        city=city,
        full_name=full_name,
        point=pos,
        avatar=user.avatar
    )


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api'):
        return make_response(jsonify({'error': 'Не найдено'}), 404)
    return render_template('404.html', title='404'), 404


@app.errorhandler(400)
def bad_request(error):
    if request.path.startswith('/api'):
        return make_response(jsonify({'error': 'Некорректный запрос'}), 400)

    return render_template('400.html',
                           title='Ошибка 400'), 400


if __name__ == '__main__':
    db_session.global_init('db/mars_explorer.db')
    app.register_blueprint(users_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')
    app.run(port=8080, host='127.0.0.1')
