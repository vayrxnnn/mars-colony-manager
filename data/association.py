import sqlalchemy

from data.db_session import SqlAlchemyBase


class Association(SqlAlchemyBase):
    __tablename__ = 'association'

    job_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey('jobs.id'),
                               primary_key=True)

    category_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('categories.id'),
                                    primary_key=True)