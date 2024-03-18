from fastapi import HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
import exceptions
from schema.output import RegisterOutput
from utils.jwt import JWTHandler
from utils.secrets import password_manager


class UsersOperations:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, username: str, password: str) -> RegisterOutput:
        hashed_password = password_manager.hash(password)
        user = User(username=username, password=hashed_password)

        async with self.db_session as session:
            # TODO: how about handle error
            try:
                session.add(user)
                await session.commit()
            except IntegrityError:
                raise exceptions.UserAlreadyExists

        return RegisterOutput(username=user.username, id=user.id)

    async def get_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise exceptions.UserNotFound

            return user_data

    async def update_username(self, old_username: str, username: str) -> User:
        query = select(User).where(User.username == old_username)
        update_query = update(User).where(User.username == old_username).values(username=username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

            await session.execute(update_query)
            await session.commit()

            user_data.username = username

            return user_data

    async def user_delete_account(self, username: str, password: str) -> None:
        delete_query = delete(User).where(User.username == username, User.password == password)

        async with self.db_session as session:
            await session.execute(delete_query)
            await session.commit()

    async def login(self, username: str, password: str) -> str:
        query = select(User).where(User.username == username)

        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise exceptions.UsernameOrPasswordIncorrect

        if not password_manager.verify(password, user.password):
            raise exceptions.UsernameOrPasswordIncorrect

        return JWTHandler.generate(username)
