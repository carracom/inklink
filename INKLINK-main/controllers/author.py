import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.author import Author
from models.db_models import AuthorDB

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_author(db: Session, author: Author) -> Author:
    try:
        db_author = AuthorDB(
            name=author.name,
            lastname=author.lastname
        )
        db.add(db_author)
        db.commit()
        db.refresh(db_author)

        return Author(
            id=str(db_author.id),
            name=db_author.name,
            lastname=db_author.lastname
        )
    except Exception as e:
        logger.exception("Error creando autor")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_all_authors(db: Session) -> list[Author]:
    try:
        authors = db.query(AuthorDB).all()
        return [
            Author(id=str(a.id), name=a.name, lastname=a.lastname)
            for a in authors
        ]
    except Exception as e:
        logger.exception("Error obteniendo autores")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_author_by_id(db: Session, author_id: int) -> Author:
    author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    return Author(id=str(author.id), name=author.name, lastname=author.lastname)


async def update_author(db: Session, author_id: int, author: Author) -> Author:
    db_author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    db_author.name = author.name
    db_author.lastname = author.lastname
    db.commit()
    db.refresh(db_author)

    return Author(id=str(db_author.id), name=db_author.name, lastname=db_author.lastname)


async def delete_author(db: Session, author_id: int) -> None:
    db_author = db.query(AuthorDB).filter(AuthorDB.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    db.delete(db_author)
    db.commit()