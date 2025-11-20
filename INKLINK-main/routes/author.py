from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.author import Author
from utils.database import get_db
from controllers.author import (
    create_author,
    get_all_authors,
    get_author_by_id,
    update_author,
    delete_author,
)

router = APIRouter()

@router.post("/", response_model=Author)
async def create_author_route(author: Author, db: Session = Depends(get_db)):
    return await create_author(db, author)

@router.get("/", response_model=list[Author])
async def get_all_authors_route(db: Session = Depends(get_db)):
    return await get_all_authors(db)

@router.get("/{author_id}", response_model=Author)
async def get_author_by_id_route(author_id: int, db: Session = Depends(get_db)):
    return await get_author_by_id(db, author_id)

@router.put("/{author_id}", response_model=Author)
async def update_author_route(author_id: int, author: Author, db: Session = Depends(get_db)):
    return await update_author(db, author_id, author)

@router.delete("/{author_id}")
async def delete_author_route(author_id: int, db: Session = Depends(get_db)):
    await delete_author(db, author_id)
    return {"message": "Autor eliminado correctamente"}