from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from textwrap import dedent

MAIN_LAYOUT = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text='К какому событию готовимся?', callback_data=str('EVENT')
            ),
            InlineKeyboardButton(
                text='О нас', callback_data=str('ABOUT_US')
            )
        ]
    ]
)

title = '''
    Добро пожаловать в FlowerShop!
    Наше приложение предлагает не просто цветы, а пышные букеты.
    Флорист поможет оформить заказ, и заложит смысл в букет, подходящий под его ситуацию!'''

WELCOME_TEXT = dedent(title)


FLOWERS = [
    'https://letoflowers.ru/upload/resize_cache/iblock/134/999_999_11c0c31f49b17127182c65cca0a6aaac1/beh2ppo946u00b69va921jpn6xgux8it.jpeg',
    'https://storage.saastra.ru/main/__sized__/uploads/products/PAVELZHDAN02296-thumbnail-1500x1500-100.jpg',
    'https://juzhnosahalinsk.grand-flora.ru/3875-10554-thickbox/amur.jpg',
]

LOGO = 'https://media.kudago.com/thumbs/xl/images/list/4e/cd/4ecd72e4c95f961e0662f78375092512.jpg'
