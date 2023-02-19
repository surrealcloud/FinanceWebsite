from . import db
from flask_login import UserMixin

class BudgetItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(100))
    itemdesc = db.Column(db.String(1000))
    itemtype = db.Column(db.String())
    itemvalue = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    budgetitem = db.relationship('BudgetItem')
