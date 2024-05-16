from typing import List

from fastapi import Depends, Request, status, HTTPException

from src.user.models import Role, User
from .auth import auth_service


class RolesAccsess:
    """
    Class for check user role

    :param allowed_roles: list of allowed roles
    :type allowed_roles: List[Role]

    :return: User has role or not
    :rtype: bool
    """

    def __init__(self, allowed_roles: List[Role]):
        self.allowed_role = allowed_roles

    async def __call__(
        self,
        request: Request,
        current_user: User = Depends(auth_service.get_current_user),
    ):
        """
        Check user role

        :param request: request
        :type request: Request

        :param current_user: current user
        :type current_user: User

        :return: User has role or not
        :rtype: bool
        """
        if not current_user:
            return False
        if current_user.role not in self.allowed_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return True
