"""Import drug bot logic"""
from drug_bot import DrugBot
from aiogram import types, F

if __name__ == "__main__":
    bot = DrugBot()

    @bot.dp.message(F.text)
    async def on_message(message: types.Message):
        """Method handling receiving message"""
        await bot.handle_message(message)

    bot.run()
