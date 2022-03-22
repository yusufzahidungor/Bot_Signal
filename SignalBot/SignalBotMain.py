import logging
from telegram.ext import *
import ccxt
import time
import pandas as pd
import talib


API_KEY = '5070773408:AAGDTl9iut4iswFGupMtyTMZjcCgEgSW0mE'
list_Symbol = ["RACA/USDT","STARL/USDT","FLOKI/USDT","BOSON/USDT","GT/USDT"]
N = 100
GATE = ccxt.gateio()


# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

def start_command(update, context):
    while True:
        for sym in list_Symbol:
            OHLCV5 = GATE.fetchOHLCV(sym, timeframe='5m', limit=N)
            df = pd.DataFrame(columns=["Open","High","Low","Close","Volume"])
            for i in range(len(OHLCV5)):
                df = df.append({"Open":OHLCV5[i][1],"High":OHLCV5[i][2],"Low":OHLCV5[i][3],"Close":OHLCV5[i][4],"Volume":OHLCV5[i][5]},ignore_index=True)
            resultRSI14 = RSI14(df)
            resultRSI7 = RSI7(df)
            resultSTOCH = STOCH(df)
            resultSAR = SAR(df)
            resultCCI = CCI(df)

            text = ""
            text = sym+"\n"+resultSAR+"\n"+resultRSI14+"\n"+resultRSI7+"\n"+resultSTOCH+"\n"+resultCCI


            if (resultRSI14 != "") | (resultRSI7 != "") | (resultSTOCH != "") | (resultCCI != ""):
                update.message.reply_text(text)
            
        time.sleep(100)

def RSI14(df):
    RSI14 = talib.RSI(df["Close"], timeperiod=14)
    len14 = len(RSI14)

    if (RSI14[len14-1] <= 30):
        result = "RSI14 < 30 :AL \n"
    elif (RSI14[len14-1] >= 70):
        result = "RSI14 > 70 : SAT \n"
    else:
        result = ""

    return result

def RSI7(df):
    RSI7 = talib.RSI(df["Close"], timeperiod=7)
    len7 = len(RSI7)

    if (RSI7[len7-1] <= 30):
        result = "RSI7 < 30 : AL ım fırsatı \n"
    elif (RSI7[len7-1] >= 70):
        result = "RSI7 > 70 : SAT ım fırsatı\n"
    else:
        result = ""

    return result

def STOCH(df):
    slowk, slowd = talib.STOCH(df["High"], df["Low"], df["Close"], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    
    if (slowk[N-1] <= 20) | (slowd[N-1] <= 20):
        result = "STOCH < 20 : AL ım fırsatı\n"
    elif (slowk[N-1] >= 80) | (slowd[N-1] >= 80):
        result = "STOCH > 80 : SAT ım fırsatı\n"
    else:
        result = ""

    return result

def SAR(df):
    SAR = talib.SAR(df["High"], df["Low"], acceleration=0.02, maximum=0.2)

    if (SAR[N-1] < df["Close"][N-1]):
        result = "SAR < CLOSE :AL ım fırsatı\n"
    elif (SAR[N-1] > df["Close"][N-1]):
        result = "SAR > CLOSE : SAT ım fırsatı\n"

    return result

def CCI(df):
    CCI = talib.CCI(df["High"], df["Low"], df["Close"], timeperiod=20)

    if CCI[N-1] < -100:
        result = "CCI < -100 : AL ım fırsatı"
    elif CCI[N-1] > 100:
        result = "CCI > -100 : SAT ım fırsatı"
    else:
        result = ""

    return result

def MACD(df):
    macd, macdsignal, macdhist = talib.MACD(df["Close"], fastperiod=12, slowperiod=26, signalperiod=9)

    if (macdhist[N-4] > macdhist[N-3]) & (macdhist[N-3] > macdhist[N-2]) & (macdhist[N-2] > macdhist[N-1]):
        result = "MACD AL ("


def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')
    update.message.reply_text("HATA")

def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()