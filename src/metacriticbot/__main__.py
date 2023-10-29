import asyncio
import telegram

from metacriticbot.config import Config

async def main():
    bot = telegram.Bot(Config.TELEGRAM_TOKEN)
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())