import yfinance as yf
import pandas as pd
import math

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
    benchmark_final = price_df.dropna()
    return benchmark_final


def compute_purchase_units(sub_price_df, asset_share, stock_money):
    result_dict = {}
    for col in sub_price_df.columns:
        price = sub_price_df[col].values[0]
        buy_amount = math.trunc(asset_share[col] * stock_money / price)
        result_dict[col] = buy_amount
    return result_dict

etflist = ['VT', 'VGLT', 'IEF', 'GSG', 'GLD']
asset_share = {'VT': 0.3, 'VGLT': 0.3, 'IEF': 0.25, 'GSG': 0.075, 'GLD': 0.075}
price_df = build_price_panel(etflist)

base_date = price_df.index[-1]
stock_money = 10000
sub_price_df = price_df.loc[price_df.index == base_date]

units = compute_purchase_units(sub_price_df, asset_share, stock_money)