import ccxt
from ccxt.huobi import huobi

print("1-Gate.io\n2-Binance\n3-BtcTurk\n4-Okex\n5-Coinbase\n6-Kucoin\n7-Ftx\n8-HitBTC\n9-Huobi\n10-Bittrex\n11-Kraken")
exc = input("Referans Borsayı seçin")

GATE = ccxt.gateio()
BINANCE = ccxt.binance()
BTCTURK = ccxt.btcturk()
OKEX = ccxt.okex()
COINBASE = ccxt.coinbasepro()
KUCOIN = ccxt.kucoin()
FTX = ccxt.ftx()
HITBTC = ccxt.hitbtc()
HUOBI = ccxt.huobipro()
BITTREX = ccxt.bittrex()
KRAKEN = ccxt.kraken()

def compare(exc1,exc2):
    pass

listSym = []
if exc == "1":
    for i in GATE.fetch_tickers():
        if ('USDT' in i) & (i.isnumeric() == False):
            listSym.append(i)
            
            gateBid = GATE.fetch_ticker(symbol=i)['bid']
            binanceBid = BINANCE.fetch_ticker(symbol=i)['bid']
            compare(gateBid,binanceBid)


            btcturkBid = BTCTURK.fetch_ticker(symbol=i)['bid']
            okexBid = OKEX.fetch_ticker(symbol=i)['bid']
            coinbaseBid = COINBASE.fetch_ticker(symbol=i)['bid']
            kucoinBid = KUCOIN.fetch_ticker(symbol=i)['bid']
            ftxBid = FTX.fetch_ticker(symbol=i)['bid']
            hitbtcBid = HITBTC.fetch_ticker(symbol=i)['bid']
            huobiBid = HUOBI.fetch_ticker(symbol=i)['bid']
            bittrexBid = BITTREX.fetch_ticker(symbol=i)['bid']
            krakenBid = KRAKEN.fetch_ticker(symbol=i)['bid']


            