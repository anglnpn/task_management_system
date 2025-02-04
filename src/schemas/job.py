from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    description: str
    author_id: int
    performer_id: int

    class Config:
        from_attributes = True


class JobCreate(BaseModel):
    title: str
    description: str
    performer_id: int
    deadline: Optional[datetime] = None


class JobCreateDB(JobBase):
    uid: UUID
    author_id: int
    performer_id: int
    deadline: Optional[datetime] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    performer_id: Optional[int] = None
    is_completed: Optional[bool] = None
    is_archived: Optional[bool] = None


class JobUpdateForPerformer(BaseModel):
    is_completed: Optional[bool] = None


class JobUpdateDB(JobUpdate):
    pass


class JobResponse(JobCreate):
    uid: UUID
    created_at: datetime
    updated_at: datetime
    is_completed: Optional[bool] = None
    is_archived: Optional[bool] = None
