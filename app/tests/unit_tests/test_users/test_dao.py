# import pytest
# from app.users.dao import UserDAO


# @pytest.mark.parametrize(
#     "user_id, email, is_exists",
#     [
#         (1, "test@test.com", True),
#         (2, "artem@example.com", True),
#         (3, "...", False),
#     ],
# )
# async def test_find_user_by_id(user_id, email, is_exists):
#     user = await UserDAO.find_by_id(user_id)

#     if is_exists:
#         assert user
#         assert user.id == user.id
#         assert user.email == email
#     else:
#         assert not user

import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "email,is_present",
    [("test@test.com", True), ("artem@example.com", True), (".....", False)],
)
async def test_find_user_by_id(email, is_present):
    user = await UserDAO.find_one_or_none(email=email)

    if is_present:
        assert user
        assert user.email == email
    else:
        assert not user
