from  src import ma, BaseSchema
from src.user.models import Tasks

class TaskSchema(BaseSchema):
    class Meta:
        model = Tasks
        exclude = ()
    id = ma.Integer(dump_only = True)
    task_name = ma.String(load = True)
    owner_id = ma.String(dump = True)