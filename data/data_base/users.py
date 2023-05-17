import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    lvl_critic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    CVSS_rating = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    EPSS_rating = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    PoC = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    CVE = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


