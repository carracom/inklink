import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.publisher import Publisher, PublisherCreate, PublisherUpdate
from models.db_models import PublisherDB, BookDB

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def create_publisher(db: Session, payload: PublisherCreate) -> Publisher:
    """
    Crea una nueva editorial.
    """
    try:
        # Validar si ya existe una editorial con el mismo nombre (opcional)
        existing = db.query(PublisherDB).filter(
            PublisherDB.name.ilike(payload.name)
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una editorial con ese nombre",
            )

        db_publisher = PublisherDB(name=payload.name)
        db.add(db_publisher)
        db.commit()
        db.refresh(db_publisher)

        return Publisher.from_orm(db_publisher)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error creando editorial")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al crear editorial: {str(e)}",
        )


async def get_publishers(db: Session) -> List[Publisher]:
    """
    Obtiene todas las editoriales.
    """
    try:
        publishers = db.query(PublisherDB).all()
        return [Publisher.from_orm(p) for p in publishers]
    except Exception as e:
        logger.exception("Error obteniendo editoriales")
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al obtener editoriales: {str(e)}",
        )


async def get_publisher_by_id(db: Session, publisher_id: int) -> Publisher:
    """
    Obtiene una editorial por ID.
    """
    publisher = db.query(PublisherDB).filter(PublisherDB.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Editorial no encontrada")

    return Publisher.from_orm(publisher)


async def update_publisher(
    db: Session, publisher_id: int, payload: PublisherUpdate
) -> Publisher:
    """
    Actualiza datos de una editorial.
    """
    try:
        db_publisher = (
            db.query(PublisherDB).filter(PublisherDB.id == publisher_id).first()
        )
        if not db_publisher:
            raise HTTPException(status_code=404, detail="Editorial no encontrada")

        update_data = payload.dict(exclude_unset=True)

        # Validar nombre duplicado si se cambia
        if "name" in update_data:
            existing = (
                db.query(PublisherDB)
                .filter(
                    PublisherDB.name.ilike(update_data["name"]),
                    PublisherDB.id != publisher_id,
                )
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe otra editorial con ese nombre",
                )

        for field, value in update_data.items():
            setattr(db_publisher, field, value)

        db.commit()
        db.refresh(db_publisher)

        return Publisher.from_orm(db_publisher)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error actualizando editorial")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al actualizar editorial: {str(e)}",
        )


async def delete_publisher(db: Session, publisher_id: int) -> None:
    """
    Elimina una editorial.
    Si tiene libros asociados, se puede bloquear el borrado.
    """
    try:
        db_publisher = (
            db.query(PublisherDB).filter(PublisherDB.id == publisher_id).first()
        )
        if not db_publisher:
            raise HTTPException(status_code=404, detail="Editorial no encontrada")

        # Verificar si hay libros asociados a esta editorial
        books_count = (
            db.query(BookDB).filter(BookDB.publisher_id == publisher_id).count()
        )
        if books_count > 0:
            raise HTTPException(
                status_code=400,
                detail="No se puede eliminar la editorial porque tiene libros asociados",
            )

        db.delete(db_publisher)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error eliminando editorial")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al eliminar editorial: {str(e)}",
        )