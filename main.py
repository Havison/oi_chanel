import asyncio
import logging
import json
import aiohttp

from pybit.unified_trading import HTTP
from config import Config, load_config
from message import message_bybit_binance, message_bybit, message_binance, message_my
from datetime import datetime, timedelta

config: Config = load_config('.env')
logger = logging.getLogger(__name__)


symbol_price = {}
binance_symbol = []
bybit_symbol = []
oi_file = 'oi.json'


def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            data_format = {key: [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in value] for key, value in data.items()}
            return data_format
    except FileNotFoundError:
        return {}


def write_file(file_name, data):
    with open(file_name, 'w') as f:
        data_format = {key: [i.strftime('%Y-%m-%d %H:%M:%S') for i in value] for key, value in data.items()}
        json.dump(data_format, f, indent=4)


async def fetch_binance_prices(session: aiohttp.ClientSession):
    url = 'https://fapi.binance.com/fapi/v2/ticker/price'
    try:
        async with session.get(url, timeout=10) as response:
            return await response.json()
    except asyncio.TimeoutError:
        logger.error("Timeout error while connecting to Binance API")
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching Binance data: {e}")
    return None


async def main():
    logging.basicConfig(
        level=logging.INFO,
        filename=f'{__name__}.log',
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await asyncio.sleep(10)
                bybit_session = HTTP(
                    testnet=False,
                    api_key=config.by_bit.api_key,
                    api_secret=config.by_bit.api_secret,
                )
                data_bybit = bybit_session.get_tickers(category="linear")
                data_binance = await fetch_binance_prices(session)
                for dicts in data_bybit['result']['list']:
                    if 'USDT' in dicts['symbol']:
                        symbol_price.setdefault(dicts['symbol'], []).append((dicts['lastPrice'], dicts['openInterest'], datetime.now(), dicts['volume24h']))
                        if dicts['symbol'] not in bybit_symbol:
                            bybit_symbol.append(dicts['symbol'])
                for data in data_binance:
                    if 'USDT' in data['symbol']:
                        if data['symbol'] not in binance_symbol:
                            binance_symbol.append(data['symbol'])
                for symbol, price in symbol_price.items():
                    dt = datetime.now() - timedelta(minutes=21)
                    for i in price:
                        quantity = read_file(oi_file)
                        dt_old = datetime.now() - timedelta(days=1)
                        if symbol in quantity:
                            if quantity[symbol][0] < dt_old:
                                quantity[symbol].remove(quantity[symbol][0])
                                write_file(oi_file, quantity)
                            if not quantity[symbol]:
                                del quantity[symbol]
                                write_file(oi_file, quantity)
                        if i[2] < dt:
                            symbol_price[symbol].remove(i)
                        try:
                            a = eval(f'({symbol_price[symbol][-1][0]} - {i[0]}) / {symbol_price[symbol][-1][0]} * 100')
                            oi = eval(f'({symbol_price[symbol][-1][1]} - {i[1]}) / {symbol_price[symbol][-1][1]} * 100')
                            volume24 = eval(f'({symbol_price[symbol][-1][3] * symbol_price[symbol][-1][0]} - {i[3] * i[0]}) / {symbol_price[symbol][-1][3]} * 100')
                            volume = int(float(symbol_price[symbol][-1][3] * symbol_price[symbol][-1][0]) - float(i[3]) * i[0])


                        except ZeroDivisionError:
                            logger.error(f'Zero division error for {symbol}')
                            continue
                        if symbol in quantity:
                            q_oi = quantity[symbol][-1] < dt
                        else:
                            q_oi = True
                        if a >= 0.01 and oi >= 3 and q_oi:
                            if symbol not in quantity:
                                quantity.setdefault(symbol, []).append(datetime.now())
                                q = 1
                                write_file(oi_file, quantity)
                                await message_my(symbol, a, oi, q, volume, volume24)
                            else:
                                quantity.setdefault(symbol, []).append(datetime.now())
                                q = len(quantity[symbol])
                                write_file(oi_file, quantity)
                            if symbol in bybit_symbol and symbol in binance_symbol:
                                await message_bybit_binance(symbol, a, oi, q, volume, volume24)
                                await asyncio.sleep(1)
                            elif symbol in binance_symbol:
                                await message_binance(symbol, a, oi, q, volume, volume24)
                                await asyncio.sleep(1)
                            else:
                                await message_bybit(symbol, a, oi, q, volume, volume24)
                                await asyncio.sleep(1)
            except Exception as e:
                logger.exception(e)
                await asyncio.sleep(3)


asyncio.run(main())









