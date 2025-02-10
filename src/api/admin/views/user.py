from typing import ClassVar

from sqladmin import ModelView

from models import User


class UserAdmin(ModelView, model=User):
    page_size = 100
    column_default_sort = ("id", True)
    column_list: ClassVar[list] = [
        User.id,
        User.uid,
        User.first_name,
        User.second_name,
        User.is_admin,
        User.is_deleted,
        User.registered_at,
        User.username,
        User.email,
    ]
    column_searchable_list: ClassVar[list] = [
        User.id,
        User.uid,
        User.first_name,
        User.second_name,
        User.username,
        User.email,
    ]
