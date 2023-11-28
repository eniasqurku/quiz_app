from agent.cons import CREATOR_GROUP_NAME
from agent.models import User


def is_creator(user: User):
    return user.is_superuser or user.groups.filter(name=CREATOR_GROUP_NAME).exists()
