import pandas as pd
import yfinance as yf
import datetime
import os


start = "2023-01-01"
end = "2024-06-30"

symbols = {
    "000001_SS": "000001.SS",
    "399001_SZ": "399001.SZ",
    "HSI": "^HSI",
    "IXIC": "^IXIC",
    "FTSE": "^FTSE",
    "GDAXI": "^GDAXI",
    "FCHI": "^FCHI",
    "600256_SS": "600256.SS",
    "filtered_data_JM0":"",
    "filtered_data_PG0":"",
    "filtered_data_SC0":""
}


output_folder = '../input/'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


dfs = []
for symbol_name in symbols.keys():
    df = pd.read_csv(os.path.join(output_folder, f"{symbol_name}.csv"), index_col='Date', parse_dates=True)
    df = df[['Close']].rename(columns={'Close': symbol_name})
    dfs.append(df)

merged_df = pd.concat(dfs, axis=1)
correlation_matrix = merged_df.corr(method="spearman")

xinjiang_correlation = correlation_matrix.loc["600256_SS"]
print("广汇能源股价走势与其他指数的相关性：")
print(xinjiang_correlation)

