import telebot
import requests

# for this we have open telegram, find father bot and then build a new bot
API_TOKEN = '<api_token>'

bot = telebot.TeleBot(API_TOKEN)

# mapping symbol -> coingecko id

COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "DOGE": "dogecoin",
    "SOL": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "ADA": "cardano"
}
def get_crypto_price(symbol):
    symbol = symbol.upper()
    if symbol not in COINS:
        return None

    coin_id = COINS[symbol]
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
    response = requests.get(url)
    data = response.json()

    price = data[coin_id]["usd"]
    change = data[coin_id]["usd_24h_change"]
    return price, change

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "Send a crypto symbol like:\nBTC\nETH\n\nOr multiple:\nBTC ETH SOL"
    )

@bot.message_handler(func=lambda message: True)
def crypto_handler(message):
    symbols = message.text.upper().split()
    results = []
    for symbol in symbols:
        data = get_crypto_price(symbol)

        if data is None:
            results.append(f"{symbol} is not a valid coin.")
            continue

        price, change = data

        results.append(
            f"{symbol}\n"
            f"Price: ${price}\n"
            f"24h Change: {change:.2f}%\n"
        )

    bot.reply_to(message, "\n".join(results))

bot.infinity_polling()
