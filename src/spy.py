import requests
import pyquery
import baostock as bs
import pandas as pd


lg = bs.login()   # 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)
rs = bs.query_history_k_data_plus("sz.399106", "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",       start_date='2024-01-01', end_date='2024-07-01',       frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

data_list = []
path = "../output/sz_399106.csv"
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
result.to_csv(path, index=False)

'''
上面那个库没有国外股票指数的数据。。。
json_url = {'http://qd.10jqka.com.cn/quote.php?cate=real&type=stock&callback=showStockDate&return=json&code=000001'}
headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
cache = requests.get(json_url,headers=headers)
print(cache)

'''