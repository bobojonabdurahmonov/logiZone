from aiogram import F, Bot, Dispatcher, types
import asyncio
import os
from youtubedownload import download_video

bot = Bot(token="Your bot token")
dp = Dispatcher()

main_lang = 'uz'

def btnentry(text, secondtext, thirdtext):
    buttonlist = types.InlineKeyboardMarkup(
        row_width = 1,
        inline_keyboard=[
            [types.InlineKeyboardButton(text=text, web_app=types.WebAppInfo(url="https://bobojonabdurahmonov.github.io/logiPlay/")),],
            [types.InlineKeyboardButton(text=secondtext, web_app=types.WebAppInfo(url="https://bobojonabdurahmonov.github.io/logiMaths/")),],
            [types.InlineKeyboardButton(text=thirdtext, callback_data="youtube")]
        ]
    )

    return buttonlist

@dp.message(F.text == "/start")
async def entry(msg: types.Message):
    language = msg.from_user.language_code
    global main_lang

    if language == 'uz':
        btns = btnentry("O'ynash🕹", "Matematik O'yin📃", "Youtubedan Yuklash✅")
        await bot.send_message(chat_id=msg.chat.id, text="Salom botimizga xush kelibsiz! Siz bu bot orqali \n\n • O'yin o'ynash \n • Matematik topshiriqlar \n • Youtubedan video yuklash \n \n ngiz mumkin. Mazza qilib foydalanishingizni tilab qolamiz!", reply_markup=btns)
        main_lang = 'uz'
    elif language == 'en':
        btns = btnentry("Play🕹", "Math Game📃", "Download Video✅")
        await bot.send_message(chat_id=msg.chat.id, text="Welcome to our bot! You can use from these functions:  \n\n • Play games \n • Math exercises \n • Download videos from youtube \n \n Happy use!", reply_markup=btns)
        main_lang = 'en'
    elif language == 'ru':
        btns = btnentry("Играть🕹","Математическая игра📃","Скачать видео✅")
        await bot.send_message(chat_id=msg.chat.id, text="""Добро пожаловать в наш бот! Вы можете пользоваться следующими функциями:

        • Играть в игры
        • Математические упражнения
        • Скачать видео с YouTube

        ! Приятного использования!""" , reply_markup=btns)
        main_lang = 'ru'

    

@dp.callback_query(F.data == "youtube")
async def downloadyoutube(call: types.CallbackQuery):
    await call.answer()
    global main_lang

    if main_lang == 'uz':
        await bot.send_message(chat_id=call.message.chat.id, text="Video yuklash uchun youtube video havolasini yuboring! (Iltimos 1 minutdan kichikroq video yuboring) ✈️")
    elif main_lang == 'en':
        await bot.send_message(chat_id=call.message.chat.id, text="Please send me url of youtube video (It's size should be under than one minute)  ✈️")
    elif main_lang == 'ru':
        await bot.send_message(chat_id=call.message.chat.id, text="Пожалуйста, отправьте мне ссылку на видео YouTube (Его длительность должна быть меньше одной минуты)✈️")
    

@dp.message(F.text)
async def replytodownload(msg: types.Message):
     global main_lang
     text = ''

     if main_lang == 'uz':
        text = await bot.send_message(chat_id=msg.chat.id, text="Biroz kuting....⏳")
     elif main_lang == 'en':
        text = await bot.send_message(chat_id=msg.chat.id, text="Just a moment....⏳")
     elif main_lang == 'ru':
         text = await bot.send_message(chat_id=msg.chat.id, text="Минутку....⏳")

     if msg.text.startswith("https://youtube.com"):
        filename = download_video(msg.text)  # haqiqiy fayl nomi

        try:
            video = types.FSInputFile(filename)  # aiogram uchun to‘g‘ri format
            await bot.delete_message(chat_id=msg.chat.id, message_id=text.message_id)
            if main_lang == 'uz':
                btns = btnentry("O'ynash🕹", "Matematik O'yin📃", "Video Yuklash✅")
            elif main_lang == 'en':
                btns = btnentry("Play🕹", "Math Game📃", "Download Video✅")
            elif main_lang == 'ru':
                btns = btnentry("Играть🕹","Математическая игра📃","Скачать видео✅")
            await bot.send_video(msg.chat.id, video, caption="✅ Mana videongiz, Yana boshqa narsalardan foydalanmoqchi bo'lsangiz 👇", reply_markup=btns)
        except Exception as e:
            await bot.send_message(msg.chat.id, f"❌ Fayl yuborishda xatolik: {e}")

        os.remove(filename)

async def init():
    await dp.start_polling(bot)

asyncio.run(init())

