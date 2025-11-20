from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from utils.database import get_db
from models.users import User, UserCreate, UserUpdate
from models.login import Login
from controllers.users import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user,
    login,
)

router = APIRouter()


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
)
async def create_user_route(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    return await create_user(db, payload)


@router.get(
    "/",
    response_model=List[User],
    summary="Listar todos los usuarios",
)
async def get_users_route(
    db: Session = Depends(get_db),
):
    return await get_users(db)


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Obtener un usuario por ID",
)
async def get_user_by_id_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    return await get_user_by_id(db, user_id)


@router.put(
    "/{user_id}",
    response_model=User,
    summary="Actualizar un usuario existente",
)
async def update_user_route(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
):
    return await update_user(db, user_id, payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un usuario",
)
async def delete_user_route(
    user_id: int,
    db: Session = Depends(get_db),
):
    await delete_user(db, user_id)
    return {"message": "Usuario eliminado correctamente"}


@router.post(
    "/login",
    summary="Login de usuario",
)
async def login_route(
    payload: Login,
    db: Session = Depends(get_db),
):
    return await login(db, payload)