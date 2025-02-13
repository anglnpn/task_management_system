from typing import List

from databases.database import get_async_session
from services.notification import notify_about_updated_jobs
from project_celery import celery_app
from utilities.async_utils import run_async


@celery_app.task
def notify_users_about_job_updated() -> str:
    async def notify_users() -> List[dict]:
        async for db in get_async_session():
            return await notify_about_updated_jobs(db=db)

    notification_result = run_async(notify_users())
    return (
        f"List of updated jobs and recipients"
        f" of sent notifications: {notification_result}"
    )
