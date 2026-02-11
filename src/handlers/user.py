from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.chat_action import ChatActionSender

from src.database import db
from src.services import ai_service

user_router = Router()

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Новый запрос")]],
    resize_keyboard=True,
    input_field_placeholder="Напиши свой вопрос..."
)

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    await db.clear_history(user_id)
    
    await message.answer(
        "Привет! Я AI-ассистент с памятью. \n"
        "Я помню контекст нашего диалога.\n\n"
        "Нажми «Новый запрос», чтобы сбросить тему.",
        reply_markup=kb
    )

@user_router.message(F.text == "Новый запрос")
async def cmd_reset(message: Message):
    await db.clear_history(message.from_user.id)
    await message.answer("♻️ Контекст сброшен. О чем поговорим теперь?", reply_markup=kb)

@user_router.message()
async def handle_ai_chat(message: Message):
    user_id = message.from_user.id
    text = message.text

    await db.add_message(user_id, "user", text)

    async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
        
        history = await db.get_last_messages(user_id)
        
        ai_response = await ai_service.generate_response(history)
        
        await db.add_message(user_id, "assistant", ai_response)
        
        await message.answer(ai_response, reply_markup=kb)