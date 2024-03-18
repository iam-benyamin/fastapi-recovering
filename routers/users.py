from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import get_db
from oprations.users import UsersOperations
from schema._input import RegisterInput, UpdateProfileInput, DeleteUserAccountInput, LoginInput

router = APIRouter(prefix="/users")


@router.post("/register")
async def register(db_session: Annotated[AsyncSession, Depends(get_db)], data: RegisterInput = Body()):
    # we also can declare db_session like this -> db_session: AsyncSession = Depends(get_db)
    user = await UsersOperations(db_session).create(username=data.username, password=data.password)

    return user


@router.post("/login")
async def login(db_session: Annotated[AsyncSession, Depends(get_db)], data: LoginInput = Body()):
    token = await UsersOperations(db_session).login(username=data.username, password=data.password)
    return token


@router.get("/{username}/")
async def get_user_profile(username: str, db_session: AsyncSession = Depends(get_db)):
    user_profile = await UsersOperations(db_session).get_by_username(username)

    return user_profile


@router.patch("/update")
async def update_user_profile(db_session: Annotated[AsyncSession, Depends(get_db)], data: UpdateProfileInput = Body()):
    user = await UsersOperations(db_session).update_username(old_username=data.old_username, username=data.username)

    return user


@router.delete("/delete/")
async def delete_user(db_session: Annotated[AsyncSession, Depends(get_db)], data: DeleteUserAccountInput = Body()):
    await UsersOperations(db_session).user_delete_account(username=data.username, password=data.password)
