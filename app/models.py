import datetime

from sqlalchemy import Text

from app import db


class Category(db.Model):
    __table_args__ = {"extend_existing": True}
    __tablename__ = 'category'

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    order = db.Column(db.Integer, default=0)
    create_time = db.Column(
        db.DateTime, default=datetime.datetime.now
    )


class Links(db.Model):
    __tablename__ = 'links'
    __table_args__ = {"extend_existing": True}

    def to_json(self):
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), default="无标题")
    link = db.Column(Text)
    goods = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    author = db.Column(db.String(32), default="匿名者")
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    create_time = db.Column(
        db.DateTime, default=datetime.datetime.now
    )
