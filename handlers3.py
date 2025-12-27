from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from db import add_user, user_exists

router = Router()

CHANNEL_USERNAME = "@Build_My_City_Announcements"

def join_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton(text="✅ Verify", callback_data="verify_join")]
    ])

@router.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    if not user_exists(user_id):
        add_user(user_id)

    try:
        member = await message.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await message.answer(
                "🏙️ *Build My City*\n\n"
                "Welcome Mayor!\n"
                "Your city journey will begin soon 🚧",
                parse_mode="Markdown"
            )
        else:
            raise TelegramBadRequest
    except:
        await message.answer(
            "🚫 To play *Build My City*, you must join our channel first.",
            reply_markup=join_keyboard(),
            parse_mode="Markdown"
        )

@router.callback_query(lambda c: c.data == "verify_join")
async def verify_join(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    try:
        member = await callback.bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            await callback.message.edit_text(
                "✅ Verification successful!\n\n"
                "🏙️ Welcome to *Build My City*.\n"
                "Game features coming soon 🚧",
                parse_mode="Markdown"
            )
        else:
            await callback.answer("❌ You haven't joined the channel yet.", show_alert=True)
    except:
        await callback.answer("⚠️ Error checking channel. Try again.", show_alert=True)
