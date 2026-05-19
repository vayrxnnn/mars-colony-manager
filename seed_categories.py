from data import db_session
from data.category import Category

db_session.global_init("db/mars_explorer.db")

db_sess = db_session.create_session()

categories_names = [
    "Инженерное дело",
    "Наука",
    "Медицина",
    "Исследования",
    "Логистика"
]

for name in categories_names:
    category = Category(name=name)
    db_sess.add(category)

db_sess.commit()

print("Категории успешно добавлены!")