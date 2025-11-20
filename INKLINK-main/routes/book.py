from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from utils.database import get_db
from models.book import Book, BookCreate, BookUpdate
from controllers.book import (
    create_book,
    get_books,
    get_book_by_id,
    update_book,
    delete_book,
)

router = APIRouter()


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo libro",
)
async def create_book_route(
    payload: BookCreate,
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo libro en la base de datos.
    """
    return await create_book(db, payload)


@router.get(
    "/",
    response_model=List[Book],
    summary="Listar libros con filtros opcionales",
)
async def get_books_route(
    title: Optional[str] = Query(None, description="Filtrar por título (like)"),
    genre: Optional[str] = Query(None, description="Filtrar por género"),
    available: Optional[bool] = Query(
        None,
        description="Filtrar por disponibilidad (true/false)",
    ),
    author_id: Optional[int] = Query(None, description="Filtrar por id de autor"),
    publisher_id: Optional[int] = Query(None, description="Filtrar por id de editorial"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Obtiene una lista de libros.  
    Se pueden aplicar filtros por título, género, disponibilidad, autor y editorial.
    """
    return await get_books(
        db,
        title=title,
        genre=genre,
        available=available,
        author_id=author_id,
        publisher_id=publisher_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{book_id}",
    response_model=Book,
    summary="Obtener un libro por ID",
)
async def get_book_by_id_route(
    book_id: int,
    db: Session = Depends(get_db),
):
    """
    Devuelve un libro específico por su ID.
    """
    return await get_book_by_id(db, book_id)


@router.put(
    "/{book_id}",
    response_model=Book,
    summary="Actualizar completamente un libro",
)
async def update_book_route(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualiza los datos de un libro.  
    Solo se modifican los campos enviados.
    """
    return await update_book(db, book_id, payload)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un libro",
)
async def delete_book_route(
    book_id: int,
    db: Session = Depends(get_db),
):
    """
    Elimina un libro por su ID.
    """
    await delete_book(db, book_id)
    return {"message": "Libro eliminado correctamente"}