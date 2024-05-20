
import asyncio

from aiogram import Bot, Dispatcher, enums

from keys import get_bot_key
from Routers.MainRouter.MainRouter import MainRouter
from Routers.WorkRouter.WorkRouter import WorkRouter
from Routers.InfoRouter.InfoRouter import InfoRouter
from Routers.RequestRouter.RequestRouter import RequestRouter

bot = Bot(get_bot_key(), parse_mode=enums.ParseMode.HTML)
dp = Dispatcher()

main_router = MainRouter(bot)
work_router = WorkRouter(bot)
info_router = InfoRouter(bot)
request_router = RequestRouter(bot)

async def main() -> None:
    dp.include_routers(
        request_router,
        info_router,
        work_router,
        main_router
    )

    poll = asyncio.create_task(dp.start_polling(bot))

    print('Bot started')

    await poll

if __name__ == "__main__":
    print('Initializing...')
    asyncio.run(main())
