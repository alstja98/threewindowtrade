import time
import pyupbit
import datetime

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
    
def get_ma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=30)
    ma30 = df['close'].rolling(30).mean().iloc[-1]
    return ma30

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

def get_before_slowd(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5")
    minutes_high = df['high'].rolling(14).max()
    minutes_low = df['low'].rolling(14).min()
    fast_k = (df['close'] - minutes_low) / (minutes_high - minutes_low) * 100
    slow_d = fast_k.rolling(3).mean()
    df = df.assign(fast_k=fast_k, slow_d=slow_d)
    before_slowd = df['slow_d'].iloc[-2]
    return before_slowd

def get_slowd(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5")
    minutes_high = df['high'].rolling(14).max()
    minutes_low = df['low'].rolling(14).min()
    fast_k = (df['close'] - minutes_low) / (minutes_high - minutes_low) * 100
    slow_d = fast_k.rolling(3).mean()
    df = df.assign(fast_k=fast_k, slow_d=slow_d)
    slowd = df['slow_d'].iloc[-1]
    return slowd
    
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit("jkTnTx1vMMbfcLkzVo0iKV7syWTPD7MzpXAo0XhU", "EZt2xYSMlP9pFx9oomel9c4xYAOqm0k92tOIrVco")
print("autotrade start")


# 자동매매 시작
while True:
    try:
        ma30 = get_ma30("KRW-ETH")
        ma60 = get_ma60("KRW-ETH")
        ma120 = get_ma120("KRW-ETH")
        beforema120 = get_before_ma120("KRW-ETH")
        before_slowd = get_before_slowd("KRW-ETH")
        slowd = get_slowd("KRW-ETH")
        current_price = get_current_price("KRW-ETH")

        if  (beforema120 < ma120) and (slowd >= 25) and (before_slowd < 25) and\
            (ma60 < current_price) and (ma120 < current_price):
             krw = get_balance("KRW")
             doge = get_balance("ETC")
             if krw > 5000:
                 if doge > 0:
                     continue
                 else:
                     upbit.buy_market_order("KRW-ETH", 6000)
        elif slowd >= 75:
            doge = get_balance("ETC")
            if doge > 0:
                upbit.sell_market_order("KRW-ETC", doge)
        elif (current_price < ma30) and (current_price < ma60) and (current_price < ma120):
            doge = get_balance("ETC")
            if doge > 0:
                upbit.sell_market_order("KRW-ETC", doge)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)