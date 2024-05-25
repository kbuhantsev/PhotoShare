from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.comments.models import Comment
from src.photos.models import Photo
from src.user.models import Role, User
from src.user.schemas import UserSchema, UserUpdateSchema


async def get_count_users(db: AsyncSession):
    """
    Count users.

    :param db: database connection
    :type db: AsyncSession
    :return: number of users
    :rtype: int
    """
    query = select(func.count(User.id))
    result = await db.execute(query)
    return result.scalar()


async def get_user_by_email(email: str, db: AsyncSession):
    """
    Retrieve a user by their email from the database.

    This function selects a user from the database by their email.

    Args:
        email (str): The email of the user to retrieve.
        db (AsyncSession): The database session.

    Returns:
        User: The user with the specified email, if it exists. Otherwise, returns None.
    """
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()

    return user


async def create_user(body: UserSchema, db: AsyncSession):
    """
    Create a new user and save it to the database.

    This function creates a new user with the provided details and saves it to the database.

    Args:
        body (UserSchema): The details of the user to create.
        db (AsyncSession): The database session.

    Returns:
        User: The newly created user.
    """
    new_user = User(**body.model_dump())
    count_users = await get_count_users(db)
    if count_users == 0:
        new_user.role = Role.ADMIN
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(email: str, body: UserUpdateSchema, db: AsyncSession):
    """
    Update a user in the database.

    This function updates a user in the database with the provided details.

    Args:
        email (User): The email of the user to update.
        body (UserUpdateSchema): The details of the user to update.
        db (AsyncSession): The database session.

    Returns:
        User: The updated user.
    """
    user = await get_user_by_email(email, db)
    if user is None:
        return None

    for attr, value in body.model_dump().items():
        setattr(user, attr, value)
    await db.commit()
    await db.refresh(user)

    return user


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    Update the avatar URL for a user in the database.

    This function retrieves a user by their email, updates their avatar URL, commits the changes to the database,
    and refreshes the user object.

    Args:
        email (str): The email of the user whose avatar is to be updated.
        url (str | None): The new avatar URL.
        db (AsyncSession): The database session.

    Returns:
        User: The updated user.
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user


async def update_password(email: str, password: str, db: AsyncSession):
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
    if user.role == role:
        return user

    user.role = role
    await db.commit()
    await db.refresh(user)
    return user


async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    Update the refresh token for a user in the database.

    This function updates the refresh token for a user and commits the changes to the database.

    Args:
        user (User): The user whose token is to be updated.
        token (str | None): The new refresh token.
        db (AsyncSession): The database session.
    """
    user.refresh_token = token
    await db.commit()


async def block_user(user: User, block: bool, db: AsyncSession):
    """
    Block or unblock a user in the database.

    This function updates the blocked flag for a user and commits the changes to the database.

    Args:
        user (User): The user to block or unblock.
        block (bool): True to block the user, False to unblock it.
        db (AsyncSession): The database session.
    :param user:
    :param block:
    :param db:
    :return:
    """

    if not user:
        return None

    if user.blocked == block:
        return user

    user.blocked = block
    await db.commit()
    await db.refresh(user)
    return user


async def get_all_users(db: AsyncSession):
    """
    Get all users.

    :param db: database connection
    :type db: AsyncSession

    :return: all users
    :rtype: List[User]
    """
    stmt = (
        select(
            User,
            func.count(Photo.id).label("count_photos"),
            func.count(Comment.id).label("count_comments"),
        )
        .select_from(User)
        .join(Photo, isouter=True)
        .join(Comment, User.id == Comment.user_id, isouter=True)
        .group_by(User.id)
    )

    result = await db.execute(stmt)

    if not result:
        return None

    users_data = result.mappings().all()

    users_profiles = []
    for user_data in users_data:
        profile = {}
        for key, value in user_data.items():
            if isinstance(value, User):
                profile.update(**value.to_dict())
            else:
                profile.update({key: value})
        users_profiles.append(profile)

    return users_profiles


async def get_user_profile(username: str, db: AsyncSession):
    """
    Get user profile.

    :param username: user username
    :type username: str
    :param db: database connection
    :type db: AsyncSession

    :return: user
    :rtype: User
    """

    stmt = (
        select(
            User,
            func.count(Photo.id).label("count_photos"),
            func.count(Comment.id).label("count_comments"),
        )
        .select_from(User)
        .filter_by(username=username)
        .join(Photo, isouter=True)
        .join(Comment, User.id == Comment.user_id, isouter=True)
        .group_by(User.id)
    )

    user_data = await db.execute(stmt)
    user_data = user_data.mappings().first()

    if not user_data:
        return None

    profile = {}
    for key, value in user_data.items():
        if isinstance(value, User):
            profile.update(**value.to_dict())
        else:
            profile.update({key: value})

    return profile


async def get_user_photos(skip: int, limit: int, user: User, db: AsyncSession):
    """
    Get user photos.

    :param user: user
    :param skip: skip
    :type skip: int
    :param limit: limit
    :type limit: int
    :param db: database connection
    :type db: AsyncSession

    :return: users photos
    :rtype: List[Photo]
    """

    # TODO: change to use src.photos
    stmt = (
        select(Photo)
        .filter_by(owner_id=user.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(Photo.tags))
    )

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_user_comments(skip: int, limit: int, user: User, db: AsyncSession):
    """
    Get user comments.

    :param user: user
    :param skip: skip
    :type skip: int
    :param limit: limit
    :type limit: int
    :param db: database connection
    :type db: AsyncSession

    :return: users comments
    :rtype: List[Comment]
    """

    # TODO
    stmt = select(Comment).filter_by(user_id=user.id).offset(skip).limit(limit)

    result = await db.execute(stmt)
    return result.scalars().all()
