from fastapi import APIRouter, HTTPException, Response, Request

from src.database import async_session_maker
from src.reposittories.users import UsersRepositories
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(first_name=data.first_name,
                            last_name=data.last_name,
                            email=data.email,
                            hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepositories(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepositories(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(requests: Request):
    if not requests.cookies:
        return None
    else:
        return {"access_token": requests.cookies["access_token"]}
