from fastapi import APIRouter

from passlib.context import CryptContext

from src.database import async_session_maker
from src.reposittories.users import UsersRepositories
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(first_name=data.first_name,
                            last_name=data.last_name,
                            email=data.email,
                            hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepositories(session).add(new_user_data)
            await session.commit()
        except Exception:
            return "Пользователь с таким email уже существует"
    return {"status": "OK"}
