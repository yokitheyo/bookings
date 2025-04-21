from fastapi import APIRouter, Depends, Response, HTTPException, status

from app.exсeptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserUpdate, SUserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException()
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me", response_model=SUserResponse)
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=SUserResponse)
async def update_user(
    user_data: SUserUpdate, current_user: Users = Depends(get_current_user)
):
    update_data = {}

    if user_data.email and user_data.email != current_user.email:
        existing_user = await UserDAO.find_one_or_none(email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        update_data["email"] = user_data.email

    if user_data.password:
        update_data["hashed_password"] = get_password_hash(user_data.password)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update",
        )

    updated_user = await UserDAO.update(current_user.id, **update_data)
    return updated_user


@router.patch("/me", response_model=SUserResponse)
async def partial_update_user(
    user_data: SUserUpdate, current_user: Users = Depends(get_current_user)
):
    update_data = {}

    if user_data.email and user_data.email != current_user.email:
        existing_user = await UserDAO.find_one_or_none(email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )
        update_data["email"] = user_data.email

    if user_data.password:
        update_data["hashed_password"] = get_password_hash(user_data.password)

    if not update_data:
        return current_user

    updated_user = await UserDAO.update(current_user.id, **update_data)
    return updated_user


@router.get("/all")
async def read_users_all(current_user: Users = Depends(get_current_admin_user)):
    return await UserDAO.find_all()
