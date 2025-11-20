from pydantic import BaseModel, constr
from typing import Optional

class PublisherBase(BaseModel):
    name: constr(min_length=1, max_length=150)


class PublisherCreate(PublisherBase):
    """Modelo para creación de editoriales."""
    pass


class PublisherUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=150)] = None


class Publisher(PublisherBase):
    id: int

    class Config:
        orm_mode = True