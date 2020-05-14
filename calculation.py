#-*-coding:utf-8-*-
import numpy as np
from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import mysql.connector
pymysql.install_as_MySQLdb()


#自定义格式转换
def convert_currency(value):
    """
    转换字符为float类型
    如果转换失败，返回0
    """
    try:
        return np.float(value)
    except Exception:
        return 0


ce = create_engine("mysql+mysqlconnector://root:coship@localhost:3306/stock", encoding='utf-8')

tabsql = "show tables"


dmtables = pd.read_sql_query(tabsql, con=ce)

#print(dmtables['Tables_in_stock'].values.tolist())

tables = dmtables['Tables_in_stock'].values.tolist()
#print(np.array(tables))
tables.remove('stname')
tables.remove('stock_sh.000001')
tables.remove('stock_sh.000002')
tables.remove('stock_sh.000003')
sql2 = "SELECT date,code,pctChg FROM `stock_sh.000001`"
data2 = pd.read_sql_query(sql2, con=ce)
#print(data2.dtypes)


# for t in tables:
#     print(t)
#     sql1 = "SELECT date,code,pctChg FROM `%s`" % t
#     data1 = pd.read_sql_query(sql1, con=ce)
#     comb = pd.concat([data2, data1], axis=1, , join='inner', ignore_index=True)


#拼接
sql3 = "SELECT date,code,pctChg FROM `stock_sh.600004`"
data3 = pd.read_sql_query(sql3, con=ce)
#print(data3['date'])
#print(data3.dtypes)
data3['pctChg'] = data3['pctChg'].astype(np.float64)
#print(data3)
comb = pd.concat([data2, data3], axis=1, join='inner', ignore_index=True)
#comb.drop_duplicates(keep='first', inplace=True)
#print((comb[5].map(lambda x: float(x)/1)))
#print(comb[5].values)

#废弃计算
#comb[6] = comb.apply(lambda x: float(x[5])/float(x[2]), axis=1)
#comb[6] = comb.apply(lambda x: {:+.2f}.format(float(x[5]))/{:+.2f}.format(float(x[2])), axis=1)
#print(comb[6].astype(np.int).values)
#print(comb.iloc[:,[2,6]])
# for i,j in comb.iloc[:,[2,6]].values:
#     #print(i, j)
#     if i > 1 and j > 2:
#         print(i,j)

comb = comb.drop_duplicates().T.drop_duplicates().T

#print(comb)
comb['vv'] = 0
#print(comb[5].values)
comb.loc[(comb[2] >= 2) & (comb.loc[:, 5] >= 3), ['vv']] = 1
print(comb['vv'].sum())
print(comb.loc[(comb.loc[:, 2] >= 2) & (comb.loc[:, 5] >= 3)])





