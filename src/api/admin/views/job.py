from typing import ClassVar

from sqladmin import ModelView

from models import Job


class JobAdmin(ModelView, model=Job):
    page_size = 100
    column_default_sort = ("id", True)
    column_list: ClassVar[list] = [
        Job.id,
        Job.uid,
        Job.author_id,
        Job.performer_id,
        Job.deadline,
        Job.is_completed,
        Job.title,
        Job.description,
        Job.created_at,
        Job.updated_at,
        Job.is_archived,
    ]
    column_searchable_list: ClassVar[list] = [
        Job.id,
        Job.title,
        Job.description,
        Job.author_id,
        Job.performer_id,
    ]
