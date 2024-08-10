import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, CHAT_ID, NEWS_TOPIC_ID, ANNOUNCES_TOPIC_ID, MAX_MANAGED_TOPICS
from database import init_db, add_topic, get_topics, update_topic_activity, get_least_active_topic, get_topic_count

# Create the bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def on_startup():
    init_db()
    await check_and_create_topics()
    print("Bot started...")


async def create_topic(title: str) -> int:
    """
    Create a new topic in the Telegram group and return its ID.
    """
    result = await bot.create_forum_topic(chat_id=CHAT_ID, name=title)
    return result.message_thread_id


async def check_and_create_topics():
    topic_count = get_topic_count()
    if topic_count < MAX_MANAGED_TOPICS:
        for _ in range(topic_count, MAX_MANAGED_TOPICS):
            new_topic_id = await create_topic("Chat: empty")
            add_topic(new_topic_id)
            print(f"Created and added new topic with ID {new_topic_id}")


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello! I'm managing topics for discussions.")


@dp.message(F.chat.type == "supergroup", F.message_thread_id.in_([NEWS_TOPIC_ID, ANNOUNCES_TOPIC_ID]))
async def handle_post_in_source_topics(message: Message):
    first_line = message.text.split('\n')[0]
    target_topic_id = get_least_active_topic()

    if not target_topic_id:
        return

    # Rename the least active topic
    await bot.edit_forum_topic(chat_id=CHAT_ID, message_thread_id=target_topic_id, name=f"Chat: {first_line}")
    await bot.forward_message(chat_id=CHAT_ID, from_chat_id=CHAT_ID, message_id=message.message_id,
                              message_thread_id=target_topic_id)
    update_topic_activity(target_topic_id)


@dp.message(F.chat.type == "supergroup")
async def track_activity(message: Message):
    topic_id = message.message_thread_id
    if topic_id:
        update_topic_activity(topic_id)


async def main():
    await on_startup()

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())