from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.dao.auto import AutoDAO
from app.dao.stats import StatsDAO
from app.dao.user import UserDAO
from app.handlers.states import SearchAuto
from app.keyboards.inline_keyboard import back_kb
from app.misc import msg
from app.misc.cmd import Command as cmd
from app.services.auto_service import AutoService
from app.services.search_sevrice import SearchService
from app.services.user_service import UserService

router = Router(name="search_commands-router")

BACK_KB = back_kb(cmd.MAIN)


@router.callback_query(StateFilter(None), F.data == cmd.SEARCH)
async def search(
    call: CallbackQuery,
    state: FSMContext,
    user_dao: UserDAO,
) -> None:
    """Обработчик перехода к поиску."""
    user = await UserService.get_user_with_auto(
        user_dao, tg_id=call.from_user.id
    )
    if user:
        if user.autos:
            await call.message.edit_text(
                msg.AUTO_ENTER_NUMBER_MSG, reply_markup=BACK_KB
            )
            await state.update_data(user_id=user.id)
            await state.set_state(state=SearchAuto.enter_number)
            return
        await call.answer(msg.NO_AUTO_MSG, True)
    await call.answer(msg.NO_DATA_MSG, True)


@router.message(SearchAuto.enter_number)
async def enter_search_number(
    message: Message,
    state: FSMContext,
    auto_dao: AutoDAO,
    stats_dao: StatsDAO,
) -> None:
    """Обработчик ввода номера автомобиля при поиске."""
    number = message.text.upper()
    if not AutoService.validate_number(number):
        await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=BACK_KB)
        return
    auto = await AutoService.get_auto(auto_dao, number)
    data = await state.get_data()
    await SearchService.add_search_try(stats_dao, data["user_id"])
    if auto is None:
        await message.answer(msg.AUTO_NOT_EXIST_MSG, reply_markup=BACK_KB)
        return
    if auto.owner.tg_id == message.from_user.id:
        await message.answer(msg.OWNER_YOUR_MSG)
        await state.clear()
        return
    await message.answer(msg.OWNER_MSG.format(auto.owner.phone))
    await state.clear()
