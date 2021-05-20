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

def get_ma90(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=90)
    ma90 = df['close'].rolling(90).mean().iloc[-1]
    return ma90

def get_ma180(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=180)
    ma180 = df['close'].rolling(180).mean().iloc[-1]
    return ma180

def get_before_ma180(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=181)
    ma180 = df['close'].rolling(180).mean().iloc[-2]
    return ma180

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
        ma30 = get_ma30("KRW-DOGE")
        ma90 = get_ma90("KRW-DOGE")
        ma180 = get_ma180("KRW-DOGE")
        beforema180 = get_before_ma180("KRW-DOGE")
        before_slowd = get_before_slowd("KRW-DOGE")
        slowd = get_slowd("KRW-DOGE")
        current_price = get_current_price("KRW-DOGE")

        if  (beforema180 < ma180) and (slowd >= 20) and (before_slowd < 20) and\
            (ma30 < current_price) and (ma90 < current_price) and (ma180 < current_price):
             krw = get_balance("KRW")
             if krw > 5000:
                 upbit.buy_market_order("KRW-DOGE", krw*0.9995)
        elif (slowd >= 70) and (before_slowd < 70):
            doge = get_balance("DOGE")
            if doge > 0.00008:
                upbit.sell_market_order("KRW-DOGE", doge*0.9995)
        elif (current_price < ma30) and (current_price < ma90) and (current_price < ma180):
            doge = get_balance("DOGE")
            if doge > 0.00008:
                upbit.sell_market_order("KRW-DOGE", doge*0.9995)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)