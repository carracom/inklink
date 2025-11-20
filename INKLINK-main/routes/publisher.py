from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from utils.database import get_db
from models.publisher import Publisher, PublisherCreate, PublisherUpdate
from controllers.publisher import (
    create_publisher,
    get_publishers,
    get_publisher_by_id,
    update_publisher,
    delete_publisher,
)

router = APIRouter()


@router.post(
    "/",
    response_model=Publisher,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva editorial",
)
async def create_publisher_route(
    payload: PublisherCreate,
    db: Session = Depends(get_db),
):
    return await create_publisher(db, payload)


@router.get(
    "/",
    response_model=List[Publisher],
    summary="Listar todas las editoriales",
)
async def get_publishers_route(
    db: Session = Depends(get_db),
):
    return await get_publishers(db)


@router.get(
    "/{publisher_id}",
    response_model=Publisher,
    summary="Obtener una editorial por ID",
)
async def get_publisher_by_id_route(
    publisher_id: int,
    db: Session = Depends(get_db),
):
    return await get_publisher_by_id(db, publisher_id)


@router.put(
    "/{publisher_id}",
    response_model=Publisher,
    summary="Actualizar una editorial",
)
async def update_publisher_route(
    publisher_id: int,
    payload: PublisherUpdate,
    db: Session = Depends(get_db),
):
    return await update_publisher(db, publisher_id, payload)


@router.delete(
    "/{publisher_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar una editorial",
)
async def delete_publisher_route(
    publisher_id: int,
    db: Session = Depends(get_db),
):
    await delete_publisher(db, publisher_id)
    return {"message": "Editorial eliminada correctamente"}