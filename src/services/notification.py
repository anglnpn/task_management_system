from datetime import datetime, UTC, timedelta
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from configs.loggers import logger
from crud.job import crud_job
from constants.email import JOB_UPDATE_MESSAGE
from utilities.email_client import send_email_notification


async def notify_about_updated_jobs(db: AsyncSession) -> List[dict]:
    one_hour_ago = datetime.now(tz=UTC) - timedelta(hours=1)
    updated_jobs_info = await crud_job.get_by_updated(
        db=db, current_datetime=one_hour_ago
    )
    if updated_jobs_info:
        for job in updated_jobs_info:
            job_title = job["title"]
            author_email = job["author_email"]
            performer_email = job["performer_email"]
            try:
                await send_email_notification(
                    recipients=[author_email, performer_email],
                    subject="Job updated",
                    body=f"<p>{JOB_UPDATE_MESSAGE + job_title}<p>",
                )
            except Exception as ex:
                msg = (
                    f"Failed to send email to"
                    f" {author_email} and {performer_email}"
                    f" with subject: {job_title}. Error: {ex}"
                )
                logger.exception(msg)

    return updated_jobs_info
