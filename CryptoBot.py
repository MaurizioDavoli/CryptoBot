import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PRICE_LINK = "is a popular site of cryptocurrencies"
TOKEN = "Your Token"
welcome_msg = "hi! Select the crypto asset and I will give you " \
              "the actual price in usd"
error_msg = "I do not know that asset, dumbass..."


def get_price(asset):
    page = requests.get(PRICE_LINK+asset)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='main-content')
    dat_list = results.find_all(class_='price')
    return dat_list[0].text


def send_msg(update, context, text):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text)


def start(update, context):
    send_msg(update, context, welcome_msg)


def assets_price(update, context):
    try:
        asset = update.message.text
        price = get_price(asset)
        send_msg(update, context, price)
    except:
        send_msg(update, context, error_msg)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    assets_handler = MessageHandler(Filters.command, assets_price)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(assets_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
