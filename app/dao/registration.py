from sqlalchemy import insert, update

from app.dao.base import BaseDAO
from app.db.models import Registrations
from app.db.database import async_session


class RegistrationsDAO(BaseDAO):
    model = Registrations

    @classmethod
    async def add_registrations(cls, tg_id):
        """Увеличить счетчик регистраций пользователя."""
        async with async_session() as session:
            registration = await cls.find_one_or_none(tg_id=tg_id)
            count = 1
            if registration:
                await session.execute(
                    update(cls.model)
                    .where(cls.model.tg_id == tg_id)
                    .values(count=registration.count + 1)
                )
                count += registration.count
            else:
                query = insert(cls.model).values(tg_id=tg_id)
                await session.execute(query)
            await session.commit()
            return count