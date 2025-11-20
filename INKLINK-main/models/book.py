from typing import Optional
from pydantic import BaseModel, Field, conint, constr

class BookBase(BaseModel):
    title: constr(min_length=1, max_length=200)
    description: Optional[str] = None
    isbn: Optional[constr(max_length=20)] = None
    genre: constr(min_length=1, max_length=50)
    publication_year: conint(ge=1400, le=2100)
    pages: Optional[conint(ge=1)] = None
    available: bool = True
    author_id: int = Field(..., description="ID del autor (FK)")
    publisher_id: int = Field(..., description="ID de la editorial (FK)")


class BookCreate(BookBase):
    """Modelo para creación de libros."""
    pass


class BookUpdate(BaseModel):
    """Modelo para actualización parcial o total."""
    title: Optional[constr(min_length=1, max_length=200)] = None
    description: Optional[str] = None
    isbn: Optional[constr(max_length=20)] = None
    genre: Optional[constr(min_length=1, max_length=50)] = None
    publication_year: Optional[conint(ge=1400, le=2100)] = None
    pages: Optional[conint(ge=1)] = None
    available: Optional[bool] = None
    author_id: Optional[int] = None
    publisher_id: Optional[int] = None


class Book(BookBase):
    id: int

    class Config:
        orm_mode = True