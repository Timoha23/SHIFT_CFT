from functools import wraps

from fastapi import HTTPException


def admin_required(func):
    """
    Декоратор проверяющий является ли текущий
    пользователь админом
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = kwargs.get("current_user")
        if current_user.is_admin:
            return await func(*args, **kwargs)
        raise HTTPException(
            status_code=403,
            detail="Недостаточно прав"
        )
    return wrapper
