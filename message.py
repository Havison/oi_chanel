from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import Config, load_config
from aiogram import Bot



config: Config = load_config('.env')
bot_oi = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )


async def message_bybit(symbol, a, oi, q):
    coinglass = f'https://www.coinglass.com/tv/ru/Bybit_{symbol}'
    bybit = f'https://www.bybit.com/trade/usdt/{symbol}'
    binance = f'https://www.binance.com/ru/futures/{symbol}'
    await bot_oi.send_message(chat_id=-1002180985919, text=f'📈<b>{symbol[0:-4]}</b>\n'
                                                  f'<b>⚫ByBit</b>\n'
                                                  f'<b>Изменения за 20 минут</b>\n'
                              f'&#128181;Цена выросла на: <b>{round(a, 2)}%</b>\n'
                              f'&#128640;Открытый интерес вырос на: <b>{round(oi, 2)}%</b>\n'
                              f'&#129535;Кол-во сигналов за 24 часа: <b>{q}</b>\n'
                                               f'<a href=\"{bybit}\">ByBit</a> | <a href=\"{coinglass}\">CoinGlass</a> | <a href=\"{binance}\">Binance</a>',
                           parse_mode='HTML', disable_web_page_preview=True)


async def message_binance(symbol, a, oi, q):
    coinglass = f'https://www.coinglass.com/tv/ru/Binance_{symbol}'
    bybit = f'https://www.bybit.com/trade/usdt/{symbol}'
    binance = f'https://www.binance.com/ru/futures/{symbol}'
    await bot_oi.send_message(chat_id=-1002180985919, text=f'📈<b>{symbol[0:-4]}</b>\n'
                                                  f'<b>🟡Binance</b>\n'
                                                  f'<b>Изменения за 20 минут</b>\n'
                              f'&#128181;Цена выросла на: <b>{round(a, 2)}%</b>\n'
                              f'&#128640;Открытый интерес вырос на: <b>{round(oi, 2)}%</b>\n'
                              f'&#129535;Кол-во сигналов за 24 часа: <b>{q}</b>\n'
                                               f'<a href=\"{binance}\">Binance</a> | <a href=\"{coinglass}\">CoinGlass</a> | <a href=\"{bybit}\">ByBit</a> ',
                           parse_mode='HTML', disable_web_page_preview=True)


async def message_bybit_binance(symbol, a, oi, q):
    coinglass = f'https://www.coinglass.com/tv/ru/Bybit_{symbol}'
    bybit = f'https://www.bybit.com/trade/usdt/{symbol}'
    binance = f'https://www.binance.com/ru/futures/{symbol}'
    await bot_oi.send_message(chat_id=-1002180985919, text=f'📈<b>{symbol[0:-4]}</b>\n'
                                                  f'<b>⚫ByBit and 🟡Binance</b>\n'
                                                  f'<b>Изменения за 20 минут</b>\n'
                                                  f'&#128181;Цена выросла на: <b>{round(a, 2)}%</b>\n'
                                                  f'&#128640;Открытый интерес вырос на: <b>{round(oi, 2)}%</b>\n'
                                                  f'&#129535;Кол-во сигналов за 24 часа: <b>{q}</b>\n'
                                                  f'<a href=\"{bybit}\">ByBit</a> | <a href=\"{coinglass}\">CoinGlass</a> | <a href=\"{binance}\">Binance</a>',
                              parse_mode='HTML', disable_web_page_preview=True)