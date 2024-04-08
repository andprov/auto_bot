from app.config import SEARCH_COUNT_LIMIT
from app.dao.stats import StatsDAO


class StatsService:
    """..."""

    @classmethod
    async def add_search_try(cls, dao: StatsDAO, user_id: int) -> None:
        """Добавить запись о поиске."""
        await dao.add(user_id=user_id)

    @classmethod
    async def check_search_access(cls, dao: StatsDAO, user_id: int) -> bool:
        """Проверить превышение лимита поисковых запросов."""
        day_search_count = await dao.get_day_search_count(user_id)
        if day_search_count < SEARCH_COUNT_LIMIT:
            return True
        return False