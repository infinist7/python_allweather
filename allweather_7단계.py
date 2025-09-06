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


def build_price_panel(etflist):
    price_df = pd.DataFrame()
    for etf in etflist:
        each_etf_df = load_and_arrange_data(etf)
        price_df = pd.merge(price_df, each_etf_df, left_index=True, right_index=True, how='outer')
    price_df = price_df.dropna()
    return price_df


def find_rebalance_schedule(price_df, start_date, end_date, freq_months):
    period_df = pd.DataFrame(price_df.loc[start_date:end_date].index)
    rebalance_schedule = []
    current_date = start_date
    while current_date < end_date:
        if current_date in period_df['Date'].values:
            rebalance_date = current_date
        else:
            rebalance_date = period_df.loc[period_df['Date'] >= current_date, 'Date'].min()
        rebalance_schedule.append(rebalance_date)
        current_date += pd.DateOffset(months=freq_months)
    if rebalance_schedule[-1] != end_date:
        rebalance_schedule.append(end_date)
    return rebalance_schedule


def run_rebalance_for_period(stock_money, sub_price_df, asset_share):
    bt_result = pd.DataFrame(index=sub_price_df.index)
    bt_result['stock_asset'] = 0
    for col in sub_price_df.columns:
        initial_buy = math.trunc(asset_share[col] * stock_money / sub_price_df[col].iloc[0])
        bt_result['stock_asset'] = (bt_result['stock_asset'] + initial_buy * sub_price_df[col])
    bt_result['cash_asset'] = stock_money - bt_result['stock_asset'].iloc[0]
    bt_result['total_asset'] = bt_result['stock_asset'] + bt_result['cash_asset']
    bt_result['daily_return'] = bt_result['total_asset'].pct_change() * 100
    return bt_result


def get_rebalance_result(rebalance_schedule, price_df, asset_share):
    stock_money = 10000
    total_bt_result = pd.DataFrame()
    for idx, _ in enumerate(rebalance_schedule[:-1]):
        sub_price_df = pd.DataFrame(price_df.loc[rebalance_schedule[idx]:rebalance_schedule[idx + 1]])
        bt_result = run_rebalance_for_period(stock_money, sub_price_df, asset_share)
        stock_money = bt_result['total_asset'].iloc[-1]
        total_bt_result = pd.concat([total_bt_result.iloc[:-1], bt_result])
    return total_bt_result


etflist = ['VT', 'VGLT', 'IEF', 'GSG', 'GLD']
price_df = build_price_panel(etflist)

start_date = price_df.index[0]
end_date = price_df.index[-1]
freq_months = 6
rebalance_schedule = find_rebalance_schedule(price_df, start_date, end_date, freq_months)

asset_share = {'VT': 0.3, 'VGLT': 0.3, 'IEF': 0.25, 'GSG': 0.075, 'GLD': 0.075}
total_bt_result = get_rebalance_result(rebalance_schedule, price_df, asset_share)


## 7단계 실습코드
year_period = (total_bt_result.index[-1].year - total_bt_result.index[0].year)
month_period = (total_bt_result.index[-1].month - total_bt_result.index[0].month) / 12
final_period = year_period + month_period

CAGR = (((total_bt_result['total_asset'].iloc[-1] / total_bt_result['total_asset'].iloc[0]) ** (1 / final_period) - 1) * 100)


max_value = np.maximum.accumulate(total_bt_result['total_asset'])
rate_value = (total_bt_result['total_asset']-max_value)/max_value
mdd = rate_value.min()*100

total_bt_result['total_asset'].plot()
plt.show(block=True)

## 함수화
def compute_cagr(total_bt_result):
    year_period = (total_bt_result.index[-1].year - total_bt_result.index[0].year)
    month_period = (total_bt_result.index[-1].month - total_bt_result.index[0].month) / 12
    final_period = year_period + month_period
    CAGR = (((total_bt_result['total_asset'].iloc[-1] / total_bt_result['total_asset'].iloc[0]) ** (1 / final_period) - 1) * 100)
    return CAGR


def compute_mdd(total_bt_result):
    max_value = np.maximum.accumulate(total_bt_result['total_asset'])
    rate_value = (total_bt_result['total_asset'] - max_value) / max_value
    mdd = rate_value.min() * 100
    return mdd

cagr = compute_cagr(total_bt_result)
mdd = compute_mdd(total_bt_result)
print(cagr, mdd)