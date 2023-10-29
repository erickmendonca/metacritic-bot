import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

from metacriticbot.client.metacritic import MetacriticClient
from metacriticbot.config import Config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def search_metacritic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = MetacriticClient().search_game(query)
    telegram_results= [(
        InlineQueryResultArticle(
            id=index,
            title=f"{result.title} - {result.score}",
            input_message_content=InputTextMessageContent(f"{result.title} ({', '.join(result.platforms)}) - {result.score}")
        )
        ) for index, result in enumerate(results)]
    await context.bot.answer_inline_query(update.inline_query.id, telegram_results)

if __name__ == '__main__':
    application = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    search_metacritic_handler = InlineQueryHandler(search_metacritic)
    application.add_handler(search_metacritic_handler)

    application.run_polling()
