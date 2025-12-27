from aiogram import Router, types
from aiogram.filters import Command
from db import add_user, user_exists

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    if not user_exists(user_id):
        add_user(user_id)

    await message.answer(
        "🏙️ *Build My City*\n\n"
        "Welcome Mayor!\n"
        "Your city journey will begin soon 🚧\n\n"
        "Stay tuned for updates.",
        parse_mode="Markdown"
    )
