from flask_login import current_user
from flask_security import RoleMixin, UserMixin
from sqlalchemy import UniqueConstraint, func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from src import db, ReprMixin, BaseMixin

class UserRole(BaseMixin, db.Model):
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'), index=True)
    role_id = db.Column(db.ForeignKey('role.id', ondelete='CASCADE'), index=True)

    user = db.relationship('User', foreign_keys=[user_id])
    role = db.relationship('Role', foreign_keys=[role_id])

    UniqueConstraint(user_id, role_id)

class Role(BaseMixin, RoleMixin, ReprMixin, db.Model):
    name = db.Column(db.String(80), unique=True, index=True)
    description = db.Column(db.String(255))
    is_hidden = db.Column(db.Boolean(), default=False, index=True)

    users = db.relationship('User', back_populates='roles', secondary='user_role')


class User(BaseMixin, ReprMixin, UserMixin, db.Model):
    __tablename__ = "user"
    __repr_fields__ = ['id', 'name']

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(127), unique=True, nullable=True, index=True)
    password = db.Column(db.String(255), nullable = False)
    name = db.Column(db.String(55), nullable=False)

    #for flask_security

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())

    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', back_populates='users', secondary='user_role')
    tasks = db.relationship("Tasks", backref = "task_owner")

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_authenticated

class Tasks(BaseMixin, ReprMixin, db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key = True, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    task_name = db.Column(db.String(120), nullable = False)