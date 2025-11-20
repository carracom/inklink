import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from models.users import User, UserCreate, UserUpdate
from models.login import Login
from models.db_models import UserDB

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_user(db: Session, payload: UserCreate) -> User:
    """
    Crea un nuevo usuario. Email único y password hasheado.
    """
    try:
        existing = db.query(UserDB).filter(UserDB.email == payload.email).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese correo electrónico",
            )

        db_user = UserDB(
            name=payload.name,
            lastname=payload.lastname,
            email=payload.email,
            password=hash_password(payload.password),
            active=payload.active,
            admin=payload.admin,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return User.from_orm(db_user)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error creando usuario")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al crear usuario: {str(e)}",
        )


async def get_users(db: Session) -> List[User]:
    """
    Obtiene todos los usuarios.
    """
    try:
        users = db.query(UserDB).all()
        return [User.from_orm(u) for u in users]
    except Exception as e:
        logger.exception("Error obteniendo usuarios")
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al obtener usuarios: {str(e)}",
        )


async def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Obtiene un usuario por ID.
    """
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return User.from_orm(user)


async def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    """
    Actualiza un usuario existente.
    """
    try:
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        update_data = payload.dict(exclude_unset=True)

        # Validar email único si se cambia
        if "email" in update_data:
            existing = (
                db.query(UserDB)
                .filter(UserDB.email == update_data["email"], UserDB.id != user_id)
                .first()
            )
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Ya existe otro usuario con ese correo electrónico",
                )

        # Si se cambia password, hashearla
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)

        return User.from_orm(db_user)

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error actualizando usuario")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al actualizar usuario: {str(e)}",
        )


async def delete_user(db: Session, user_id: int) -> None:
    """
    Elimina un usuario por ID.
    """
    try:
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        db.delete(db_user)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error eliminando usuario")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al eliminar usuario: {str(e)}",
        )


async def login(db: Session, payload: Login) -> dict:
    """
    Login básico: valida email y contraseña.
    """
    try:
        user = db.query(UserDB).filter(UserDB.email == payload.email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if not verify_password(payload.password, user.password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if not user.active:
            raise HTTPException(status_code=403, detail="Usuario inactivo")

        # Aquí podrías generar un JWT si quieres.
        return {
            "message": "Login exitoso",
            "user": {
                "id": user.id,
                "name": user.name,
                "lastname": user.lastname,
                "email": user.email,
                "active": user.active,
                "admin": user.admin,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error en login de usuario")
        raise HTTPException(
            status_code=500,
            detail=f"Error en la base de datos al procesar login: {str(e)}",
        )