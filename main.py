import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("./7203.csv")

print(data.loc[:, ["日付", "始値", "高値", "安値", "終値", "出来高"]].head(3))

# 日付,終値データを抽出
closing_prices = data.loc[:, ["日付","終値"]]
# カンマを削除して数値に変換
closing_prices["終値"] = closing_prices["終値"].str.replace(',', '').astype(float)
# 日付をdatetime形式に変換
closing_prices["日付"] = pd.to_datetime(closing_prices["日付"])

# トヨタ自動車の株式分割の情報
split_date = pd.Timestamp("2021-09-29")
split_ratio = 5

closing_prices.loc[closing_prices["日付"] < split_date, "終値"] = closing_prices.loc[closing_prices["日付"] < split_date, "終値"] / split_ratio

print(closing_prices.head(3))

plt.plot(closing_prices.loc[:, "日付"], closing_prices.loc[:, "終値"], label="closing price")
plt.title("closing_price", fontsize=16)  # タイトル
plt.xlabel("date", fontsize=12)       # x軸ラベル
plt.ylabel("price", fontsize=12)       # y軸ラベル
plt.legend()                         # 凡例を表示

plt.show()


