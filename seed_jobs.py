from data import db_session
from data.jobs import Jobs
from data.category import Category

db_session.global_init("db/mars_explorer.db")

db_sess = db_session.create_session()

jobs_data = [
    {
        "job": "Настройка системы жизнеобеспечения",
        "team_leader": 1,
        "work_size": 18,
        "collaborators": "2, 6",
        "is_finished": False,
        "categories": [1, 2]
    },
    {
        "job": "Исследование образцов марсианского грунта",
        "team_leader": 3,
        "work_size": 26,
        "collaborators": "1, 4",
        "is_finished": True,
        "categories": [3, 4]
    },
    {
        "job": "Ремонт солнечных панелей",
        "team_leader": 6,
        "work_size": 14,
        "collaborators": "2",
        "is_finished": False,
        "categories": [2, 5]
    },
    {
        "job": "Медицинское обследование экипажа",
        "team_leader": 5,
        "work_size": 8,
        "collaborators": "1, 3, 6",
        "is_finished": True,
        "categories": [6]
    },
    {
        "job": "Подготовка экспедиции в северный сектор",
        "team_leader": 4,
        "work_size": 30,
        "collaborators": "1, 2, 3",
        "is_finished": False,
        "categories": [1, 4, 5]
    }
]

for data in jobs_data:
    job = Jobs(
        job=data["job"],
        team_leader=data["team_leader"],
        work_size=data["work_size"],
        collaborators=data["collaborators"],
        is_finished=data["is_finished"]
    )

    db_sess.add(job)

    for category_id in data["categories"]:
        category = db_sess.get(Category, category_id)

        if category:
            job.categories.append(category)

db_sess.commit()

print("Работы успешно добавлены!")