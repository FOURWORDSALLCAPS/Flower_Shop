import logging

from environs import Env
from telegram import Update
from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
)
from root_handler_callbacks import (
    start,
    stop,
    about_us,
    go_main,
    send_flower
)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def return_to_start(update: Update, context: CallbackContext) -> str:
    update.callback_query.message.reply_text(
        'К сожалению мы не можем оформить заказ без Вашего разрешения :('
    )
    context.user_data['came_from'] = 'disagree'
    start(update, context)

    return 'DISAGREE'


def stop_nested(update: Update, context: CallbackContext) -> str:
    """Completely end conversation from within nested conversation."""
    send_flower(update)

    return 'STOPPING'


def main():
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher

    root_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'SELECTING_SCENARIO': [
                CallbackQueryHandler(about_us, pattern='^ABOUT_US$'),
                CallbackQueryHandler(go_main, pattern='^MAIN$'),
            ],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(root_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
