# Trendy-Botimport logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from reddit_scraper import fetch_reddit_trends  # Our new module

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN_HERE'  # Replace this

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello Henry! Hustle Bot is online and ready to hunt trends for you.'
    )

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text('⚠️ Please specify a task to run, e.g. `/run reddit`')
        return

    task = context.args[0].lower()

    if task == 'reddit':
        await update.message.reply_text('🔍 Fetching Reddit trends, one sec...')
        trends = fetch_reddit_trends()
        response = '🔥 Reddit Trending Topics:\n' + '\n'.join(f"- {t}" for t in trends)
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(f'❌ Unknown task: {task}')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('run', run))

    print('Bot is polling...')
    app.run_polling()
