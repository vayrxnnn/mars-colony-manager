from data import db_session
from data.users import User

db_session.global_init("db/mars_explorer.db")

db_sess = db_session.create_session()

users_data = [
    {
        "surname": "Орлова",
        "name": "Елизавета",
        "age": 22,
        "position": "Командир",
        "speciality": "Пилот",
        "address": "module_1",
        "email": "orloveee@mail.com",
        "city_from": "Владивосток",
        "password": "123456",
        "avatar": "avatar6.jpg"
    },
    {
        "surname": "Иванов",
        "name": "Алексей",
        "age": 28,
        "position": "Инженер",
        "speciality": "Системный инженер",
        "address": "module_1",
        "email": "alexey@example.com",
        "city_from": "Москва",
        "password": "123456",
        "avatar": "avatar1.jpg"
    },
    {
        "surname": "Смирнова",
        "name": "Мария",
        "age": 31,
        "position": "Биолог",
        "speciality": "Исследователь",
        "address": "module_2",
        "email": "maria@example.com",
        "city_from": "Санкт-Петербург",
        "password": "123456",
        "avatar": "avatar2.jpg"
    },
    {
        "surname": "Петров",
        "name": "Дмитрий",
        "age": 35,
        "position": "Астронавт-исследователь",
        "speciality": "Пилот",
        "address": "science_module_4",
        "email": "dmitry@example.com",
        "city_from": "Казань",
        "password": "123456",
        "avatar": "avatar3.jpg"
    },
    {
        "surname": "Кузнецова",
        "name": "Анна",
        "age": 26,
        "position": "Врач",
        "speciality": "Хирург",
        "address": "medical_module",
        "email": "anna@example.com",
        "city_from": "Новосибирск",
        "password": "123456",
        "avatar": "avatar4.jpg"
    },
    {
        "surname": "Волков",
        "name": "Игорь",
        "age": 40,
        "position": "Техник",
        "speciality": "Механик",
        "address": "tech_module",
        "email": "igor@example.com",
        "city_from": "Екатеринбург",
        "password": "123456",
        "avatar": "avatar5.jpg"
    }
]

for data in users_data:
    user = User(
        surname=data["surname"],
        name=data["name"],
        age=data["age"],
        position=data["position"],
        speciality=data["speciality"],
        address=data["address"],
        email=data["email"],
        city_from=data["city_from"],
        avatar=data["avatar"]
    )

    user.set_password(data["password"])

    db_sess.add(user)

db_sess.commit()

print("Пользователи успешно добавлены!")