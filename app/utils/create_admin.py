import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Salary, User
from db.session import async_session
from utils.hashing import Hasher


async def create_admin():
    session: AsyncSession = async_session()

    async with session.begin():
        query = select(User).where(User.username == "admin")
        admin = await session.scalar(query)
        if admin is None:
            admin = User(
                username="admin",
                password=Hasher.hash_password("admin"),
                email="admin@admin.ru",
                first_name="admin",
                last_name="admin",
                role="admin"
            )
            salary = Salary()
            admin.salary = salary
            session.add(admin)
        else:
            if admin.role != "admin":
                admin.role = "admin"


async def main():
    task = asyncio.create_task(create_admin())
    await task


if __name__ == "__main__":
    asyncio.run(main())
