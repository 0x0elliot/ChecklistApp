from src.utils import ModelResource
from src.user.models import Tasks
from .schemas import TaskSchema


class TaskResource(ModelResource):

    model = Tasks
    schema = TaskSchema

    auth_required = True

    exclude = {'owner_email',}

    