from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import User, Role
from src.user.schemas import UserSchema


async def get_user_by_email(email: str, db: AsyncSession):
    """
    Get user by email.

    Returns user with the specified email or None if no such user exists.

    :param email: user email
    :type email: str
    :param db: database connection
    :type db: AsyncSession
    :return: user
    :rtype: User
    """

    query = select(User).filter(User.email == email)
    result = await db.execute(query)

    return result.scalar_one_or_none()


async def create_user(body: UserSchema, db: AsyncSession):
    """
    Create new user.

    :param body: user data
    :type body: UserSchema
    :param db: database connection
    :type db: AsyncSession

    :return: created user
    :rtype: User
    """
    user = User(**body.model_dump(exclude_unset=True))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update user token.

    :param user: user
    :type user: User
    :param token: new token
    :type token: str
    :param db: database connection
    :type db: AsyncSession

    :return: updated user
    :rtype: User
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: AsyncSession):
    """
    Confirm user email.

    :param email: user email
    :type email: str
    :param db: database connection
    :type db: AsyncSession

    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(user: User, avatar_url: str, db: AsyncSession):
    """
    Update user avatar.

    :param user: user
    :type user: User
    :param avatar_url: new avatar url
    :type avatar_url: str
    :param db: database connection
    :type db: AsyncSession

    :return: updated user
    :rtype: User
    """
    user.avatar = avatar_url
    await db.commit()
    await db.refresh(user)
    return user


async def update_password(email: User, password: str, db: AsyncSession):
    """
    Update user password.

    :param email: user email
    :type email: User
    :param password: new password
    :type password: str
    :param db: database connection
    :type db: AsyncSession

    :return: updated user
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.password = password
    await db.commit()
    await db.refresh(user)
    return user


async def update_role(user: User, role: Role, db: AsyncSession):
    """
    Update user role.

    :param user: user
    :type user: User
    :param role: new role
    :type role: Role
    :param db: database connection
    :type db: AsyncSession

    :return: updated user
    :rtype: User
    """
    user.role = role
    await db.commit()
    await db.refresh(user)
    return user
