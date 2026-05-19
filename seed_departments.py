from data import db_session
from data.departments import Department

db_session.global_init("db/mars_explorer.db")

db_sess = db_session.create_session()

departments_data = [
    {
        "title": "Engineering Department",
        "chief": 1,
        "members": "1, 5",
        "email": "engineering@mars.org"
    },
    {
        "title": "Science Department",
        "chief": 2,
        "members": "2, 3, 6",
        "email": "science@mars.org"
    },
    {
        "title": "Medical Department",
        "chief": 4,
        "members": "4",
        "email": "medical@mars.org"
    },
    {
        "title": "Exploration Department",
        "chief": 3,
        "members": "1, 2, 3",
        "email": "exploration@mars.org"
    },
    {
        "title": "Logistics Department",
        "chief": 5,
        "members": "5, 6",
        "email": "logistics@mars.org"
    }
]

for data in departments_data:
    department = Department(
        title=data["title"],
        chief=data["chief"],
        members=data["members"],
        email=data["email"]
    )

    db_sess.add(department)

db_sess.commit()

print("Департаменты успешно добавлены!")