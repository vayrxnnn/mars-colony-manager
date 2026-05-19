import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)

    jobs = orm.relationship("Jobs",
                            secondary="association",
                            back_populates="categories")