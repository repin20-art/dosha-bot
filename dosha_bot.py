import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

API_TOKEN = "8252877532:AAGLvxowp2DpQo0sw4iyplcFKCk8dVrF-tQ"  # вставь свой токен от BotFather

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ---- Состояния ----
class TestStates(StatesGroup):
    waiting_for_start = State()
    asking_question = State()


# ---- Вопросы ----
questions = [
    "Какое у тебя телосложение?",
    "Какая у тебя кожа?",
    "Как ты переносишь холод?",
    "Как ты переносишь жару?",
    "Как у тебя с аппетитом?",
    "Какая у тебя походка?",
    "Какой у тебя сон?",
    "Как ты обычно реагируешь на стресс?",
    "Насколько быстро ты устаешь?",
    "Какой у тебя голос?",
    "Как быстро ты говоришь?",
    "Ты склонен к полноте?",
    "Ты склонен к худобе?",
    "Ты быстро запоминаешь информацию?",
    "Ты надолго запоминаешь информацию?",
    "Как ты обычно проявляешь эмоции?",
    "Насколько активен твой ум?",
    "Ты больше любишь сладкое или солёное?",
    "Как у тебя с выносливостью?",
    "Насколько тебе свойственен перфекционизм?",
    "Как часто у тебя бывает раздражительность?",
    "Ты любишь физическую активность?",
    "Какой у тебя уровень энергии утром?",
    "Какой у тебя уровень энергии вечером?"
]

# Варианты ответов
answer_options = [
    ["Худощавое", "Среднее", "Крупное"],
    ["Сухая", "Нормальная", "Жирная"],
    ["Плохо", "Нормально", "Хорошо"],
    ["Плохо", "Нормально", "Хорошо"],
    ["Плохой", "Средний", "Очень хороший"],
    ["Лёгкая", "Обычная", "Тяжёлая"],
    ["Лёгкий", "Средний", "Глубокий"],
    ["Тревога", "Гнев", "Спокойствие"],
    ["Быстро", "Средне", "Медленно"],
    ["Тонкий", "Нормальный", "Громкий"],
    ["Быстро", "Средне", "Медленно"],
    ["Да", "Иногда", "Нет"],
    ["Да", "Иногда", "Нет"],
    ["Быстро", "Средне", "Медленно"],
    ["Нет", "Средне", "Да"],
    ["Ярко", "Умеренно", "Сдержанно"],
    ["Очень активен", "Умеренно", "Спокоен"],
    ["Сладкое", "И то, и другое", "Солёное"],
    ["Низкая", "Средняя", "Высокая"],
    ["Очень", "Иногда", "Не особо"],
    ["Редко", "Иногда", "Часто"],
    ["Да", "Иногда", "Нет"],
    ["Низкий", "Средний", "Высокий"],
    ["Низкий", "Средний", "Высокий"]
]


# ---- Команда /start ----
@dp.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Старт")]],
        resize_keyboard=True
    )
    await state.set_state(TestStates.waiting_for_start)
    await message.answer(
        "✨ Добро пожаловать в <b>DoshaBot</b>!\n\n"
        "Этот тест поможет определить твою <i>дошу</i> 🪐\n"
        "Нажми <b>Старт</b>, чтобы начать космическое путешествие.",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


# ---- Начало теста ----
@dp.message(F.text == "🚀 Старт", TestStates.waiting_for_start)
async def start_test(message: types.Message, state: FSMContext):
    await state.update_data(current_q=0, answers=[])
    await state.set_state(TestStates.asking_question)
    await ask_question(message, state)


async def ask_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_index = data["current_q"]

    if q_index < len(questions):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=opt) for opt in answer_options[q_index]]],
            resize_keyboard=True
        )
        await message.answer(f"❓ {questions[q_index]}", reply_markup=keyboard)
    else:
        await show_result(message, state)


# ---- Ответы ----
@dp.message(TestStates.asking_question)
async def process_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_index = data["current_q"]
    answers = data["answers"]

    answers.append(message.text)
    q_index += 1
    await state.update_data(current_q=q_index, answers=answers)

    if q_index < len(questions):
        await ask_question(message, state)
    else:
        await show_result(message, state)


# ---- Результат ----
async def show_result(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answers = data["answers"]

    # Простейшая логика: считаем количество вариантов
    vata = answers.count("Худощавое") + answers.count("Сухая") + answers.count("Плохо")
    pitta = answers.count("Среднее") + answers.count("Нормальная") + answers.count("Гнев")
    kapha = answers.count("Крупное") + answers.count("Жирная") + answers.count("Спокойствие")

    if vata > pitta and vata > kapha:
        dosha = "🌬️ Вата"
        recommendations = (
            "✨ Рекомендации:\n"
            "- Избегай холода и сухости\n"
            "- Больше тёплой и питательной пищи\n"
            "- Регулярный режим сна\n"
            "- Йога, дыхательные практики"
        )
    elif pitta > vata and pitta > kapha:
        dosha = "🔥 Питта"
        recommendations = (
            "✨ Рекомендации:\n"
            "- Избегай перегрева и стресса\n"
            "- Больше овощей и охлаждающих продуктов\n"
            "- Регулярные прогулки на свежем воздухе\n"
            "- Практикуй медитацию"
        )
    else:
        dosha = "💧 Капха"
        recommendations = (
            "✨ Рекомендации:\n"
            "- Избегай переедания и тяжёлой пищи\n"
            "- Больше активности и движения\n"
            "- Лёгкий режим питания\n"
            "- Контрастный душ и спорт"
        )

    await message.answer(
        f"🌌 Твой космический результат:\n\n"
        f"<b>{dosha}</b>\n\n"
        f"{recommendations}",
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove()
    )

    await state.clear()


# ---- Запуск ----
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
