from select import select

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from icecream import ic  # Assuming you're using the 'icecream' library for debugging
from sqlalchemy import select, insert, update,and_
from sqlalchemy.exc import SQLAlchemyError

from bot.buttons.inline import *
from bot.buttons.reply import menu_btn
from bot.buttons.text import *
from bot.handlers.ai_utils import *
from bot.handlers.ppt_utils import create_presentation
from bot.state.main import PPTState, ReferatState
from db.connect import session
from db.model import User
from dispatcher import dp
from aiogram.types import FSInputFile

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        text="Assalomu alaykum!\n"
"📕Taqdimot - tugmasini bosib taqdimot yaratishni boshlashingiz mumkin.\n"
"📘Referat/Mustaqil ish - Referat yoki Mustaqil ish tayorlash uchun.\n"
"📃Qo'llanma - botdan qanday foydalanish haqida ma'lumot.\n Iltimos, avval shu bo'lim bilan tanishib chiqing.\n"
"/info - ma'lumot qidirish uchun."
"❓Savol va takliflar: @shokh_smee",
        reply_markup=menu_btn()
    )
    query = insert(User).values(chat_id=message.from_user.id)
    session.execute(query)
    session.commit()

@dp.message(lambda msg : msg.text == presentation_txt)
async def register_handler(msg : Message , state : FSMContext):
    await state.set_state(PPTState.ppt_name)
    await msg.answer("Presentatsiya mavzusini 3 ta so'zdan ko'p to'liq va bexato kiriting:")


@dp.message(PPTState.ppt_name)
async def from_whom_handler(msg : Message , state : FSMContext):
    data = await state.get_data()
    data["ppt_name"] = msg.text
    await state.set_data(data)
    await state.set_state(PPTState.ppt_slide_count)
    await msg.answer(text="Presentatsiya slide sonini kiriting(minimum: 8 ta slide) :")

@dp.message(PPTState.ppt_slide_count)
async def ppt_slide_number(msg :Message , state : FSMContext):
    data = await state.get_data()
    data["ppt_slide_count"] = msg.text
    topic = msg.text.strip()
    ppt_slide_titles = generate_slide_title(slide_number=data["ppt_slide_count"],
                                            previous_titles=data.get('ppt_name'),
                                            api_key=OPENAI_API_KEY,
                                            prompt=data.get('ppt_name'))
    presentation_content = generate_unique_slide_content(api_key=OPENAI_API_KEY,
                                                         slide_title=ppt_slide_titles,
                                                         prompt=data.get('ppt_name'),
                                                         )
    ppt_ready = create_presentation(data.get('ppt_name'),
                                    data["ppt_slide_count"],
                                    OPENAI_API_KEY,
                                    OPENAI_API_KEY)
    await msg.answer(f"Creating a presentation for: {topic}...")



    if not ppt_ready:
        await msg.answer("Sorry, I couldn't generate content for your topic. Please try again.")
        return

    # Create presentation
    filename = create_presentation(topic, ppt_ready)

    # Send the generated presentation
    file = FSInputFile(filename)
    await msg.answer_document(file)
    await msg.answer("Here is your presentation!")
    await state.clear()




@dp.message(lambda msg : msg.text == referat_mustaqil_ish_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer(text="Malumotlar bexato ekanligiga ishonch xosil qiling\n")
    await state.set_state(ReferatState.univer_name)
    await msg.answer(text="Institut va kafedrangizni to'liq kiriting.\n"
"📋Namuna: FARG‘ONA POLITEXNIKA INSTITUTI KIMYO TEXNALOGIYA KAFEDRASI")


@dp.message(ReferatState.univer_name)
async def message_callback(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data["univer_name"] = msg.text
    await state.set_data(state_data)
    await state.set_state(ReferatState.referat_mavzusi)
    await msg.answer("Referat mavzusini kiriting:")

@dp.message(ReferatState.referat_mavzusi)
async def message_callback(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data["referat_mavzusi"] = msg.text
    await state.set_data(state_data)
    await state.set_state(ReferatState.referat_muallif)
    await msg.answer("Muallif ism-familiyasi, guruhi va hokazolarni to'liq kiriting.\n\n"
"📋Namuna: Aliyev Alibek, 4-kurs, 23-guruh")

@dp.message(ReferatState.referat_muallif)
async def message_callback(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    state_data["referat_muallif"] = msg.text
    await state.set_data(state_data)
    await state.set_state(ReferatState.referat_tili)
    await msg.answer("🇺🇿 Tilni tanlang",reply_markup=TIL())

@dp.callback_query(ReferatState.referat_tili)
async def from_whom_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    data = await state.get_data()
    data["referat_tili"] = call.data
    await state.set_data(data)
    await state.set_state(ReferatState.referat_sahifa_soni)
    await call.message.answer("🇺Sahifalar sonini oraliq ko'rinishida tanlang", reply_markup=Sahifalar_soni())

@dp.callback_query(ReferatState.referat_sahifa_soni)
async def getting_ready(call : CallbackQuery , state : FSMContext):
    state_data = await state.get_data()
    state_data["referat_sahifa_soni"] = call.data
    await state.set_data(state_data)
    warning_message = (
        "❗ Referat tayyorlash uchun balansingizda yetarlicha mablag' mavjud emas.\n\n"
        "Referat narxi:\n"
        f"• {state_data.get("referat_sahifa_soni")} - 10000 so'm\n\n"
        "💰 Balansingiz: 0"
    )
    await call.answer(warning_message,show_alert=True)

@dp.message(lambda msg : msg.text == balans_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer(text="💰Balansingiz: 0 so'm\n"
"/referal - do'stlarni taklif qilib balansni to'ldirish🔗\n"
"/my - barcha ma'lumotlaringiz.\n\n"
"Balansingizda pul qolmagan. Balansingizni 2xil usulda to'ldirishingiz mumkin:\n\n"

"1. Bepul - /referal buyrug'ini yuboring, do'stlaringizni taklif qiling. Har bir botga qo'shilgan do'stingiz uchun 1000 so'mdan oling!"
"2. To'lov usulida - /buy buyrug'ini yuboring va kartaga to'lov qilib chekni yuboring!")

@dp.message(lambda msg : msg.text == referal_txt)
async def register_handler(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user = session.query(User).filter(User.chat_id == user_id).first()
    if user:    # Generate referral link
        referral_url = f"https://t.me/share/url?url=/https://t.me/rxso_testbot?start={user_id}"

        await msg.reply(
            f"🔗 Sizning referal linkingiz:\n{referral_url}\n\n"
            f"Do'stlaringizni taklif qiling va har bir yangi foydalanuvchi uchun 5000 so'mga ega bo'ling!"
        ,
        reply_markup=send())


@dp.message(lambda msg : msg.text == balans_txt)
async def register_handler(msg: Message, state: FSMContext):
    await msg.answer(text="💰Balansingiz: 0 so'm\n"
"/referal - do'stlarni taklif qilib balansni to'ldirish🔗\n"
"/my - barcha ma'lumotlaringiz.\n\n"
"Balansingizda pul qolmagan. Balansingizni 2xil usulda to'ldirishingiz mumkin:\n\n"

"1. Bepul - /referal buyrug'ini yuboring, do'stlaringizni taklif qiling. Har bir botga qo'shilgan do'stingiz uchun 1000 so'mdan oling!"
"2. To'lov usulida - /buy buyrug'ini yuboring va kartaga to'lov qilib chekni yuboring!")

@dp.message(lambda msg : msg.text == buy_txt)
async def register_handler(msg: Message, state: FSMContext):
        await msg.reply(
            "Qaysi usulda to'lov qilmoqchisiz❓ Quyidagi tugmalardan foydalaning👇"
        ,
        reply_markup=buy_method())