from telegram import (
    Update,
    MessageEntity,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import CallbackContext
from random import choice

from buttons import MAIN_LAYOUT, WELCOME_TEXT, FLOWERS, LOGO


def start(update: Update, context: CallbackContext) -> str:
    bold_entity = MessageEntity(type=MessageEntity.BOLD, offset=0, length=29)
    came_from = context.user_data.get('came_from')
    if not came_from:
        update.message.reply_photo(
            LOGO,
            caption=WELCOME_TEXT,
            reply_markup=MAIN_LAYOUT,
            caption_entities=[bold_entity],
        )
    elif came_from == 'disagree':
        update.callback_query.answer()
        update.callback_query.message.reply_photo(
            LOGO,
            caption=WELCOME_TEXT,
            reply_markup=MAIN_LAYOUT,
            caption_entities=[bold_entity],
        )
    elif came_from == 'go_main':
        update.callback_query.answer()
        update.callback_query.edit_message_caption(
            WELCOME_TEXT,
            reply_markup=MAIN_LAYOUT,
            caption_entities=[bold_entity],
        )

    context.user_data['came_from'] = None
    return 'SELECTING_SCENARIO'


def send_flower(update):
    flower = choice(FLOWERS)
    update.message.reply_photo(flower)


def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    send_flower(update)

    return -1


def about_us(update: Update, context: CallbackContext) -> str:
    buttons = [
        [
            InlineKeyboardButton(text='Назад', callback_data=str('MAIN')),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.edit_message_caption(
        str('О НАС КРЧ'), reply_markup=keyboard
    )


def go_main(update: Update, context: CallbackContext) -> str:
    context.user_data['came_from'] = 'go_main'
    start(update, context)
