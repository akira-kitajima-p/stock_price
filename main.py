import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from easyesn import PredictionESN

data = pd.read_csv("./7203.csv")

print(data.loc[:, ["日付", "始値", "高値", "安値", "終値", "出来高"]].head(3))

# 日付,終値データを抽出
closing_prices = data.loc[:, ["日付", "始値", "高値", "安値", "終値", "出来高"]]
# 日付をdatetime形式に変換
closing_prices["日付"] = pd.to_datetime(closing_prices["日付"])
# カンマを削除して数値に変換
closing_prices["始値"] = closing_prices["始値"].str.replace(',', '').astype(float)
closing_prices["終値"] = closing_prices["終値"].str.replace(',', '').astype(float)
closing_prices["高値"] = closing_prices["高値"].str.replace(',', '').astype(float)
closing_prices["安値"] = closing_prices["安値"].str.replace(',', '').astype(float)
closing_prices["出来高"] = closing_prices["出来高"].str.replace(',', '').astype(float)

# トヨタ自動車の株式分割の情報
split_date = pd.Timestamp("2021-09-29")
split_ratio = 5

# 分割前の株価を調整
closing_prices.loc[closing_prices["日付"] < split_date, "始値"] = closing_prices.loc[closing_prices["日付"] < split_date, "始値"] / split_ratio
closing_prices.loc[closing_prices["日付"] < split_date, "終値"] = closing_prices.loc[closing_prices["日付"] < split_date, "終値"] / split_ratio
closing_prices.loc[closing_prices["日付"] < split_date, "高値"] = closing_prices.loc[closing_prices["日付"] < split_date, "高値"] / split_ratio
closing_prices.loc[closing_prices["日付"] < split_date, "安値"] = closing_prices.loc[closing_prices["日付"] < split_date, "安値"] / split_ratio
# 出来高は倍にしてみる
closing_prices.loc[closing_prices["日付"] < split_date, "出来高"] = closing_prices.loc[closing_prices["日付"] < split_date, "出来高"] * split_ratio

# mplfinanceで認識できるように変換
closing_prices.set_index("日付", inplace=True)
closing_prices = closing_prices.rename(columns={"日付": "Date","始値": "Open", "高値": "High", "安値": "Low", "終値": "Close", "出来高": "Volume"})

print(closing_prices.head(100))

# # ローソク足チャートを描画
# fig, axes = mpf.plot(closing_prices.head(100), type="candle", volume=True, style="yahoo", returnfig= True)
# # x軸を逆転させる
# axes[0].invert_xaxis()  # ローソク足チャートのx軸を逆転
# mpf.show()

# easyesnで株価を予測する
# 前半7割を訓練用、後半7割をテスト用に使う
train = closing_prices[:int(len(closing_prices)*0.7)]
test  = closing_prices[int(len(closing_prices)*0.7):]

# ある日までの株価データから1日後の株価を予測するモデルを作成する
x_train = train[:-1]
y_train = train[1:]
x_test = test[:-1]
y_test = test[1:]

print(x_train.head(100))
print(y_train.head(100))


esn = PredictionESN(n_input=5,n_reservoir=100,n_output=5)
esn.fit(x_train.to_numpy(), y_train.to_numpy(), transientTime=100, verbose=1)

y_test_pred = esn.predict(x_test.to_numpy())


# 結果をプロット
plt.figure(figsize=(12, 6))
plt.plot(y_test.index, y_test["Close"], label="Actual")
plt.plot(y_test.index, y_test_pred[:, 3], label="Predicted")
plt.legend()
plt.title("Stock Price Prediction")
plt.show()

