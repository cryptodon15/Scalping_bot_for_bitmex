from datetime import datetime as dt
import requests, pytz
import pandas as pd
#import mpl_finance as mpf
from collections import OrderedDict
#import matplotlib
#import matplotlib.pyplot as plt


class Get_Indicator:

    def __init__(self):
        # 初期設定
        self.REQUESTS_URL = 'https://www.bitmex.com/api/udf/history?symbol=XBTUSD&resolution={t_res}&from={t_from}&to={t_to}'


    def df_ohlcv(self, time_range=1, bar_no=500):
        # ohlcvの取得
        t_to = int(dt.now(pytz.utc).timestamp())
        t_from = t_to - time_range * 60 * bar_no
        row_ohlcv = requests.get(self.REQUESTS_URL.format(t_res=time_range, t_from=t_from, t_to=t_to))
        json_ohlcv = row_ohlcv.json()
        list_ohlcv = [list(ohlcv) for ohlcv in zip(json_ohlcv["t"], json_ohlcv["o"], json_ohlcv["h"], json_ohlcv["l"], json_ohlcv["c"], json_ohlcv["v"])]
        df_ohlcv = pd.DataFrame(list_ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])

        # 日時データをDataFrameのインデックスにする
        df_ohlcv["datetime"] = pd.to_datetime(df_ohlcv["timestamp"], unit="s")
        df_ohlcv = df_ohlcv.set_index("datetime")
        pd.to_datetime(df_ohlcv.index, utc=True)

        return df_ohlcv


    def ta_sma(self, df_ohlcv, ma_range=15):
        # 移動平均（SMA：Simple Moving Average）の算出
        df_key = 'SMA' + str(ma_range)
        df_sma = pd.DataFrame(OrderedDict({
                                    df_key: df_ohlcv['close'].rolling(ma_range).mean()
                                }))
        return df_sma


    def ta_hl(self, df_ohlcv, ma_range=15):
        # hlバンド
        df_key = 'HL' + str(ma_range)
        df_max = pd.DataFrame(OrderedDict({
                                    df_key: df_ohlcv['close'].rolling(ma_range).max()
                                }))
        df_min = pd.DataFrame(OrderedDict({
                                    df_key: df_ohlcv['close'].rolling(ma_range).min()
                                }))
        return df_max,df_min

    def ta_sma_plot(self, df_ohlcv, df_sma, ma_range=10, bar_no=120):
        # 描画領域を作成
        fig = plt.figure(figsize=(20,20))
        ax = plt.subplot(1,1,1)

        # チャート表示数にDataFrameをトリミング
        df_ohlcv = df_ohlcv.iloc[-(bar_no)-1:]
        df_sma   = df_sma.iloc[-(bar_no)-1:]

        # ロウソクチャートをプロット
        mpf.candlestick2_ohlc(ax,
                              opens     = df_ohlcv["open"],
                              highs     = df_ohlcv["high"],
                              lows      = df_ohlcv["low"],
                              closes    = df_ohlcv["close"],
                              width     = 0.8,
                              colorup   = "#46AE74",
                              colordown = "#E4354A")

        # x軸をdateにする
        xdate = df_ohlcv.index 
        x_int_list = range(0, len(xdate), 6)
        ax.set_xticks(x_int_list)
        ax.set_xticklabels((xdate[int(x)].strftime('%d %H:%M') for x in x_int_list))

        # x軸の整形 
        fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')

        # グラフの両サイドをトリム
        ax.set_xlim([-1, bar_no+1])

        # 移動平均（SMA：Simple Moving Average）をプロット
        df_sma.reset_index(inplace=True)
        df_key = 'SMA' + str(ma_range)
        ax.plot(df_sma[df_key], color='Blue', linewidth='1.0', label=df_key)

        # グラフの描画
        plt.show()


def main():
    ma_range=10
    ta = Get_Indicator()
    df_ohlcv = ta.df_ohlcv(time_range=60, bar_no=500)
    df_sma = ta.ta_sma(df_ohlcv, ma_range=ma_range)
    ta.ta_sma_plot(df_ohlcv, df_sma, ma_range=ma_range, bar_no=120)


if __name__ == '__main__':
    main()