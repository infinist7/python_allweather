### 이전 단계까지의 코드 작업
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
def load_and_arrange_data(etfname):
    item_df = yf.Ticker(etfname).history(period='max')
    item_df = item_df.rename(columns={'Close': etfname})
    item_df = item_df[[etfname]]
    return item_df

def build_price_panel(etflist):
    price_df = pd.DataFrame()
    for etf in etflist:
        each_etf_df = load_and_arrange_data(etf)
        price_df = pd.merge(price_df, each_etf_df, left_index=True, right_index=True, how='outer')
    price_df = price_df.dropna()
    return price_df

etflist = ['VT','VGLT','IEF','GSG','GLD']
price_df = build_price_panel(etflist)


## 4단계 실습코드
start_date = price_df.index[0]
end_date = price_df.index[-1]
freq_months = 6

period_df = pd.DataFrame(price_df.loc[start_date:end_date].index)
rebalance_schedule = []
current_date = start_date
while current_date <= end_date:
    if current_date in period_df['Date'].values:
        rebalance_date = current_date
    else:
        rebalance_date = period_df.loc[period_df['Date'] >= current_date, 'Date'].min()
    rebalance_schedule.append(rebalance_date)
    current_date += pd.DateOffset(months=freq_months)
if rebalance_schedule[-1] != end_date:
    rebalance_schedule.append(end_date)


## 함수화
def find_rebalance_schedule(price_df, start_date, end_date, freq_months):
    period_df = pd.DataFrame(price_df.loc[start_date:end_date].index)
    rebalance_schedule = []
    current_date = start_date
    while current_date < end_date:
        if current_date in period_df['Date'].values:
            rebalance_date = current_date
        else:
            rebalance_date = period_df.loc[period_df['Date'] >= current_date,'Date'].min()
        rebalance_schedule.append(rebalance_date)
        current_date += pd.DateOffset(months=freq_months)
    if rebalance_schedule[-1] != end_date:
        rebalance_schedule.append(end_date)
    return rebalance_schedule

start_date = price_df.index[0]
end_date = price_df.index[-1]
freq_months = 6
rebalance_schedule = find_rebalance_schedule(price_df, start_date, end_date, freq_months)
