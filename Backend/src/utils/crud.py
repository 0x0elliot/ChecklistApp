from sqlalchemy import schema
from src import tasks
from src.tasks.schemas import TaskSchema
from src.user.models import User, Tasks
from src.user import models
from src.user.schemas import UserSchema

from werkzeug.security import generate_password_hash, check_password_hash

def get_user(user_id : int):
    return models.User.query.filter(models.User.id == user_id).first()

def get_user_by_email(db, email : str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db, limit: int, skip : int):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_task(task_id, owner_id):
    db_task = Tasks.query.filter(models.Tasks.id == task_id).filter(models.Tasks.user_id == owner_id).first()
    return db_task

def get_tasks(owner_id):
    db_tasks = Tasks.query.filter(models.Tasks.user_id == owner_id)
    return db_tasks

def create_user(db, user: UserSchema):
    password = generate_password_hash(user.password, method = 'sha256')
    db_user = models.User(email = user.email, name = user.name, password = password)
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user

def create_task(db, task_name, owner):
    db_task = models.Tasks(task_name = task_name, task_owner = owner)
    db.session.add(db_task)
    db.session.commit()
    db.session.refresh(db_task)
    return db_task

def delete_task(db, task_id : int):
    db_task = Tasks.query.filter(Tasks.id == task_id).first()
    if db_task:
        db.session.delete(db_task)
        db.session.commit()
        return True
    else:
        return False

def verify_password(user, password):
    return check_password_hash(password = password, pwhash = user.password)
