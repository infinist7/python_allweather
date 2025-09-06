## 이전 단계까지의 코드 작업
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


item_df = load_and_arrange_data('VT')
item_df_vglt = load_and_arrange_data('VGLT')


## 3단계 실습코드
price_df = pd.DataFrame()
price_df = pd.merge(price_df, item_df, left_index=True, right_index=True,how='outer')
price_df = pd.merge(price_df, item_df_vglt, left_index=True, right_index=True, how='outer')


## 함수화
def build_price_panel(etflist):
    price_df = pd.DataFrame()
    for etf in etflist:
        each_etf_df = load_and_arrange_data(etf)
        price_df = pd.merge(price_df, each_etf_df, left_index=True, right_index=True, how='outer')
    price_df = price_df.dropna()
    return price_df

etflist = ['VT','VGLT','IEF','GSG','GLD']
price_df = build_price_panel(etflist)
