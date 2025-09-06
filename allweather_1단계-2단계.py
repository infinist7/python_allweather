## 1단계 실습코드
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np


## 2단계 실습코드
etfname = 'VT'
item_df = yf.Ticker(etfname).history(period='max')
item_df = item_df.rename(columns={'Close': etfname})
item_df = item_df[[etfname]]

etfname = 'VGLT'
item_df_vglt = yf.Ticker(etfname).history(period='max')
item_df_vglt = item_df_vglt.rename(columns={'Close':etfname})
item_df_vglt = item_df_vglt[[etfname]]

## 함수화
def load_and_arrange_data(etfname):
    item_df = yf.Ticker(etfname).history(period='max')
    item_df = item_df.rename(columns={'Close': etfname})
    item_df = item_df[[etfname]]
    return item_df


item_df = load_and_arrange_data('VT')
item_df_vglt = load_and_arrange_data('VGLT')