import asyncio

from aiogram import Bot, Dispatcher, enums
from aiogram.client.default import DefaultBotProperties

from config import config

from Utils.BotStorage import BotStorage

from Routers.ExtraRouter.ExtraRouter import ExtraRouter
from Routers.MainRouter.MainRouter import MainRouter
from Routers.PartnershipRouter.PartnershipRouter import PartnershipRouter
from Routers.JoinUsRouter.JoinUsRouter import JoinUsRouter
from Routers.InfoRouter.InfoRouter import InfoRouter
from Routers.RequestRouter.RequestRouter import RequestRouter
from Routers.DefaultRouter.DefaultRouter import DefaultRouter


default_properties = DefaultBotProperties(parse_mode=enums.ParseMode.HTML)
bot_token = config.bot_api_token

bot = Bot(bot_token, default=default_properties)

BotStorage().load_data()
user_storage = BotStorage().load_storage()

dp = Dispatcher(storage=user_storage)

extra_router = ExtraRouter(bot)

main_router = MainRouter(bot)
partnership_router = PartnershipRouter(bot)
work_with_us_router = JoinUsRouter(bot)
info_router = InfoRouter(bot)
request_router = RequestRouter(bot)
default_router = DefaultRouter(bot)


def reload_assets() -> None:
    main_router.reload_assets()
    partnership_router.reload_assets()
    work_with_us_router.reload_assets()
    info_router.reload_assets()
    request_router.reload_assets()
    default_router.reload_assets()


extra_router.set_reload_assets_callback(reload_assets)


def poll_keyboard() -> None:
    while True:
        print("Enter 'exit' to stop: ")
        command = input()
        if not command:
            continue
        elif command == "unload_data":
            BotStorage().unload_data(dp)
        if command == "exit":
            break
        else:
            print(f"Unknown command {command}")


async def main() -> None:
    dp.include_routers(
        extra_router,
        main_router,
        request_router,
        info_router,
        partnership_router,
        work_with_us_router,
        default_router,
    )

    await bot.delete_webhook()

    bot_poll = asyncio.create_task(dp.start_polling(bot))
    keyboard_poll = asyncio.to_thread(poll_keyboard)

    print("Bot started")

    await keyboard_poll

    print("Stopping bot...")
    await dp.stop_polling()
    await bot_poll

    print("Bot stopped. Saving data...")
    BotStorage().unload_data(dp)

    print("Exiting...")


if __name__ == "__main__":
    print("Initializing...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        asyncio.run(dp.storage.close())
        print("Stopped")
