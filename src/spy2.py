import yfinance as yf
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


start = "2023-01-01"
end = "2024-06-30"

symbols = {
    "恒生指数": "^HSI",
    "纳斯达克": "^IXIC",
    "英国富时100指数": "^FTSE",
    "德国DAX指数": "^GDAXI",
    "法国CAC40指数": "^FCHI",
    "新疆本地上市企业": "600256.SS",
    "上证指数": "000001.SS",
    "深证指数": "399001.SZ",
}


futures_symbols = {
    "煤炭期货": "ZC",
    "石油期货": "SC",
    "天然气期货": "NG"
}


output_folder = '../output/'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


data = {}


for symbol_name, ticker in symbols.items():
    df = yf.download(ticker, start=start, end=end)
    data[symbol_name] = df[['Close']].rename(columns={'Close': symbol_name})
    print(f"已获取 {symbol_name} 的数据")
    df.to_csv(os.path.join(output_folder, f"{symbol_name}.csv"))


for future_name, future_code in futures_symbols.items():

    df = ak.get_futures_daily(symbol=future_code, start_date=start, end_date=end, adjust="qfq")
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    df = df[['close']].rename(columns={'close': future_name})
    data[future_name] = df
    print(f"已获取 {future_name} 的数据")
    df.to_csv(os.path.join(output_folder, f"{future_name}.csv"))



merged_df = pd.concat(data.values(), axis=1)


correlation_matrix = merged_df.corr()


xinjiang_correlation = correlation_matrix.loc["新疆本地上市企业"]
print("新疆本地上市企业与其他指数及期货的相关性：")
print(xinjiang_correlation)

# 数据可视化
plt.figure(figsize=(14, 8))
for column in merged_df.columns:
    plt.plot(merged_df.index, merged_df[column], label=column)

plt.title('股票指数及期货价格走势')
plt.xlabel('日期')
plt.ylabel('收盘价')
plt.legend()
plt.grid(True)
plt.show()
