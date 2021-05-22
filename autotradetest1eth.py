import time
import pyupbit


access = "jkTnTx1vMMbfcLkzVo0iKV7syWTPD7MzpXAo0XhU"
secret = "EZt2xYSMlP9pFx9oomel9c4xYAOqm0k92tOIrVco"

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_before_ma10(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=11)
    ma10 = df['close'].rolling(10).mean().iloc[-2]
    return ma10

def get_ma10(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=10)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

def get_ma20(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=20)
    ma10 = df['close'].rolling(20).mean().iloc[-1]
    return ma10

def get_before_ma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=31)
    ma30 = df['close'].rolling(30).mean().iloc[-2]
    return ma30

def get_ma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=30)
    ma30 = df['close'].rolling(30).mean().iloc[-1]
    return ma30

def get_before_ma60(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=61)
    ma60 = df['close'].rolling(60).mean().iloc[-2]
    return ma60

def get_ma60(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=60)
    ma60 = df['close'].rolling(60).mean().iloc[-1]
    return ma60

def get_ma120(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=120)
    ma120 = df['close'].rolling(120).mean().iloc[-1]
    return ma120

def get_before_ma120(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=121)
    ma120 = df['close'].rolling(120).mean().iloc[-2]
    return ma120

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit("jkTnTx1vMMbfcLkzVo0iKV7syWTPD7MzpXAo0XhU", "EZt2xYSMlP9pFx9oomel9c4xYAOqm0k92tOIrVco")
print("autotrade start")


# 자동매매 시작
while True:
    try:
        ma10 = get_ma10("KRW-ETH")
        ma20 = get_ma20("KRW-ETH")
        ma30 = get_ma30("KRW-ETH")
        ma60 = get_ma60("KRW-ETH")
        ma120 = get_ma120("KRW-ETH")
        beforema10 = get_before_ma10("KRW-ETH")
        beforema30 = get_before_ma30("KRW-ETH")
        beforema60 = get_before_ma60("KRW-ETH")
        beforema120 = get_before_ma120("KRW-ETH")
        current_price = get_current_price("KRW-ETH")

        if  (beforema120 < ma120) and (beforema10 < ma10) and (beforema30 < ma30) and (beforema60 < ma60) and\
            (ma60 < current_price) and (ma120 < current_price) and (ma10 < current_price) and (ma30 < current_price):
             krw = get_balance("KRW")
             doge = get_balance("ETH")
             if krw > 5000:
                 if doge > 0:
                     continue
                 else:
                     upbit.buy_market_order("KRW-XRP", 6000)
        elif current_price < ma20:
            doge = get_balance("ETH")
            if doge > 0:
                upbit.sell_market_order("KRW-ETH", doge)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)