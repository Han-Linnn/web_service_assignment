import datetime
from app import db


class Url(db.Model):
    id = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String(2040))
    short = db.Column("short", db.String(5), unique=True)

    def __init__(self, long, short):
        self.long = long
        self.short = short

    # def __repr__(self):
    #     return '<URL %s>' % self.long
