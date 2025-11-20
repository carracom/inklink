import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.book import Book, BookCreate, BookUpdate
from models.db_models import BookDB, AuthorDB, PublisherDB

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def create_book(db: Session, payload: BookCreate) -> Book:
    """
    Crea un libro nuevo validando que existan autor y editorial.
    """
    try:
        # Validar existencia de autor
        author = db.query(AuthorDB).filter(AuthorDB.id == payload.author_id).first()
        if not author:
            raise HTTPException(status_code=400, detail="Autor no encontrado")

        # Validar existencia de editorial
        publisher = (
            db.query(PublisherDB)
            .filter(PublisherDB.id == payload.publisher_id)
            .first()
        )
        if not publisher:
            raise HTTPException(status_code=400, detail="Editorial no encontrada")

        # Validar ISBN único si se envía
        if payload.isbn:
            existing = db.query(BookDB).filter(BookDB.isbn == payload.isbn).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe un libro con ese ISBN",
                )

        db_book = BookDB(
            title=payload.title,
            description=payload.description,
            isbn=payload.isbn,
            genre=payload.genre,
            publication_year=payload.publication_year,
            pages=payload.pages,
            available=payload.available,
            author_id=payload.author_id,
            publisher_id=payload.publisher_id,
        )

        db.add(db_book)
        db.commit()
        db.refresh(db_book)

        return Book.from_orm(db_book)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error creando libro")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al crear libro: {str(e)}",
        )


async def get_books(
    db: Session,
    title: Optional[str] = None,
    genre: Optional[str] = None,
    available: Optional[bool] = None,
    author_id: Optional[int] = None,
    publisher_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
) -> List[Book]:
    """
    Obtiene una lista de libros con filtros opcionales.
    """
    try:
        query = db.query(BookDB)

        if title:
            query = query.filter(BookDB.title.ilike(f"%{title}%"))
        if genre:
            query = query.filter(BookDB.genre.ilike(f"%{genre}%"))
        if available is not None:
            query = query.filter(BookDB.available == available)
        if author_id is not None:
            query = query.filter(BookDB.author_id == author_id)
        if publisher_id is not None:
            query = query.filter(BookDB.publisher_id == publisher_id)

        docs = query.offset(skip).limit(limit).all()

        return [Book.from_orm(b) for b in docs]

    except Exception as e:
        logger.exception("Error obteniendo libros")
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al obtener libros: {str(e)}",
        )


async def get_book_by_id(db: Session, book_id: int) -> Book:
    """
    Obtiene un libro por su ID.
    """
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return Book.from_orm(book)


async def update_book(db: Session, book_id: int, payload: BookUpdate) -> Book:
    """
    Actualiza un libro existente (PUT/PATCH).
    """
    try:
        db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        # Si se cambia autor/editorial, validar que existan
        if payload.author_id is not None:
            author = db.query(AuthorDB).filter(AuthorDB.id == payload.author_id).first()
            if not author:
                raise HTTPException(status_code=400, detail="Autor no encontrado")

        if payload.publisher_id is not None:
            publisher = (
                db.query(PublisherDB)
                .filter(PublisherDB.id == payload.publisher_id)
                .first()
            )
            if not publisher:
                raise HTTPException(status_code=400, detail="Editorial no encontrada")

        # Validar ISBN único si se cambia
        if payload.isbn is not None:
            existing = (
                db.query(BookDB)
                .filter(
                    and_(
                        BookDB.isbn == payload.isbn,
                        BookDB.id != book_id,
                    )
                )
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe otro libro con ese ISBN",
                )

        # Actualizar solo campos enviados
        update_data = payload.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_book, field, value)

        db.commit()
        db.refresh(db_book)

        return Book.from_orm(db_book)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error actualizando libro")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al actualizar libro: {str(e)}",
        )


async def delete_book(db: Session, book_id: int) -> None:
    """
    Elimina un libro por ID.
    """
    try:
        db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
        if not db_book:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        db.delete(db_book)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error eliminando libro")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al eliminar libro: {str(e)}",
        )