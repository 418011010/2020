#-*-coding:utf-8-*-
import numpy as np
from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MO, TU
from datetime import datetime
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import mysql.connector
from tqdm import tqdm
pymysql.install_as_MySQLdb()


#自定义格式转换
def convert(value):
    """
    转换字符为float类型
    如果转换失败，返回0
    """
    try:
        return np.float(value)
    except Exception:
        return 1


ce = create_engine("mysql+mysqlconnector://root:coship@localhost:3306/stock", encoding='utf-8')
tabsql = "show tables"
dmtables = pd.read_sql_query(tabsql, con=ce)
tables = dmtables['Tables_in_stock'].values.tolist()
#print(np.array(tables))
tables.remove('stname')
tables.remove('stock_sh.000001')
tables.remove('stock_sh.000002')
tables.remove('stock_sh.000003')
tables.remove('stock_sz.399001')
sql1 = "SELECT date,code,pctChg,close FROM `stock_sh.603429`"
data1 = pd.read_sql_query(sql1, con=ce)
sql2 = "SELECT date,code,pctChg FROM `stock_sz.399001`"
data2 = pd.read_sql_query(sql2, con=ce)
data2['pctChg'] = data2['pctChg'].apply(convert)



#print(data1)

data1['30d'] = data1['close'].rolling(30).mean()
#print(data1[['date', 'close', '30d']])
data1['30d'] = data1['30d'].apply(convert)
data1['close'] = data1['close'].apply(convert)
data1['ratio'] = data1['close'] / data1['30d']
#print(data1)
#data1.set_index('date')
#data1 = data1.set_index(data1['date']).sort_index()
#data1 = data1.fillna(0)
print(data1)
data1 = data1.set_index(data1['date']).sort_index()
fig1 = plt.figure(figsize=(16, 6))
ax1 = fig1.add_subplot(1,1,1)
#data1['ratio'].plot(label='比值')

plt.rcParams['font.sans-serif'] = ['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus'] = False
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(TU, interval=3))
xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in data1['date']]
#xmajorLocator = MultipleLocator(5)  # 定义横向主刻度标签的刻度差为2的倍数。就是隔几个刻度才显示一个标签文本
plt.plot(xs, data1['ratio'], label='test')
plt.xticks(size='small', rotation=45, fontsize=13)
ax1.legend(loc='upper left')
plt.show()




#
# for t in tables:
#     #print(t)
#     if t[7] == 'h':
#         sql3 = "SELECT date,code,pctChg FROM `%s`" % t
#         data3 = pd.read_sql_query(sql3, con=ce)
#         data3['pctChg'] = data3['pctChg'].apply(convert_currency)
#         comb = pd.concat([data1, data3], axis=1, join='inner', ignore_index=True)
#         comb = comb.drop_duplicates().T.drop_duplicates().T
#         comb['v'] = 0
#         comb.loc[(comb[2] <= 0) & (comb.loc[:, 5] >= 3), ['v']] = 1
#         if comb['v'].sum() >= 30:
#             print(t)
#             print(comb['v'].sum())
#     elif t[7] == 'z':
#         sql4 = "SELECT date,code,pctChg FROM `%s`" % t
#         data4 = pd.read_sql_query(sql4, con=ce)
#         data4['pctChg'] = data4['pctChg'].apply(convert_currency)
#         comb = pd.concat([data2, data4], axis=1, join='inner', ignore_index=True)
#         comb = comb.drop_duplicates().T.drop_duplicates().T
#         comb['v'] = 0
#         comb.loc[(comb[2] <= 0) & (comb.loc[:, 5] >= 3), ['v']] = 1
#         if comb['v'].sum() >= 30:
#             print(t)
#             print(comb['v'].sum())
#
#




