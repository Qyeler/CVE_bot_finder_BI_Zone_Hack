from typing import List

from data.data_base import db_session

from data.data_base.users import User

db_session.global_init("./data/data_base.db")
session = db_session.create_session()

def change_user_info(user_id, info):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user: 
        session.close()
        return 0
    for inf in info:
        if inf == "CVSS_rating":
            user.CVSS_rating = info[inf]
        if inf == "EPSS_rating":
            user.EPSS_rating = info[inf]
        if inf == "lvl_critic":
            user.lvl_critic = info[inf]
        if inf == "date":
            user.date = info[inf]
        if inf == "PoC":
            user.PoC = info[inf]
        if inf == "CVE":
            user.CVE = info[inf]
    session.commit()
    session.close()
    return 1

def get_user_info(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        session.close()
        return {}
    resp = {"CVE": user.CVE, 
            "CVSS_rating" : user.CVSS_rating,
            "EPSS_rating" : user.EPSS_rating, 
            "date" : user.date, 
            "lvl_critic" : user.lvl_critic,
            "PoC" : user.PoC,
            "id" : user.id}
    session.close()
    return resp



def null_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        session.close()
        return 0
    user.CVE = False
    user.CVSS_rating = None
    user.EPSS_rating = None
    user.date = None
    user.lvl_critic = None
    user.PoC = False
    session.commit()
    session.close()
    return 1


def add_user(info):
    session = db_session.create_session()
    user = User()
    for inf in info:
        if inf == "CVSS_rating":
            user.CVSS_rating = info[inf]
        if inf == "EPSS_rating":
            user.EPSS_rating = info[inf]
        if inf == "lvl_critic":
            user.lvl_critic = info[inf]
        if inf == "date":
            user.date = info[inf]
        if inf == "PoC":
            user.PoC = info[inf]
        if inf == "CVE":
            user.CVE = info[inf]
    session.add(user)
    session.commit()
    session.close()

def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        session.close()
        return 0
    session.delete(user)
    session.commit()
    session.close()
    return 1