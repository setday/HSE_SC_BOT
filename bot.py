
import asyncio

from aiogram import Bot, Dispatcher, enums

from keys import get_bot_key
from Routers.MainRouter.MainRouter import MainRouter
from Routers.PartnershipRouter.PartnershipRouter import PartnershipRouter
from Routers.WorkWithUsRouter.WorkWithUsRouter import WorkWithUsRouter
from Routers.InfoRouter.InfoRouter import InfoRouter
from Routers.RequestRouter.RequestRouter import RequestRouter

bot = Bot(get_bot_key(), parse_mode=enums.ParseMode.HTML)
dp = Dispatcher()

main_router = MainRouter(bot)
partnership_router = PartnershipRouter(bot)
work_with_us_router = WorkWithUsRouter(bot)
info_router = InfoRouter(bot)
request_router = RequestRouter(bot)

async def main() -> None:
    dp.include_routers(
        request_router,
        info_router,
        partnership_router,
        work_with_us_router,
        main_router
    )

    # await bot.delete_webhook()

    poll = asyncio.create_task(dp.start_polling(bot))

    print('Bot started')

    await poll

if __name__ == "__main__":
    print('Initializing...')
    asyncio.run(main())
