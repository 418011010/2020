#-*-coding:utf-8-*-
import numpy as np
from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from tqdm import tqdm
import time
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
tables = dmtables['Tables_in_stock'].values.tolist()
#print(np.array(tables))
tables.remove('stname')
tables.remove('stock_sh.000001')
tables.remove('stock_sh.000002')
tables.remove('stock_sh.000003')
tables.remove('stock_sz.399001')
sql1 = "SELECT date,code,pctChg FROM `stock_sh.000001`"
data1 = pd.read_sql_query(sql1, con=ce)
sql2 = "SELECT date,code,pctChg FROM `stock_sz.399001`"
data2 = pd.read_sql_query(sql2, con=ce)
data2['pctChg'] = data2['pctChg'].apply(convert_currency)
#print(data2.dtypes)

pbar = tqdm(tables)
for t in pbar:
    pbar.set_description("processing %s" % t)
    #print(t)
    if t[7] == 'h':
        sql3 = "SELECT date,code,pctChg FROM `%s`" % t
        data3 = pd.read_sql_query(sql3, con=ce)
        data3['pctChg'] = data3['pctChg'].apply(convert_currency)
        comb = pd.concat([data1, data3], axis=1, join='inner', ignore_index=True)
        comb = comb.drop_duplicates().T.drop_duplicates().T
        comb['v'] = 0
        comb.loc[(comb[2] <= 0) & (comb.loc[:, 5] >= 3), ['v']] = 1
        if comb['v'].sum() >= 30:
            print(t)
            print(comb['v'].sum())
    elif t[7] == 'z':
        sql4 = "SELECT date,code,pctChg FROM `%s`" % t
        data4 = pd.read_sql_query(sql4, con=ce)
        data4['pctChg'] = data4['pctChg'].apply(convert_currency)
        comb = pd.concat([data2, data4], axis=1, join='inner', ignore_index=True)
        comb = comb.drop_duplicates().T.drop_duplicates().T
        comb['v'] = 0
        comb.loc[(comb[2] <= 0) & (comb.loc[:, 5] >= 3), ['v']] = 1
        if comb['v'].sum() >= 30:
            print(t)
            print(comb['v'].sum())

# #拼接
# sql3 = "SELECT date,code,pctChg FROM `stock_sh.600004`"
# data3 = pd.read_sql_query(sql3, con=ce)
# data3['pctChg'] = data3['pctChg'].astype(np.float64)
# #print(data3)
# comb = pd.concat([data2, data3], axis=1, join='inner', ignore_index=True)
# comb = comb.drop_duplicates().T.drop_duplicates().T
# comb['vv'] = 0
# comb.loc[(comb[2] >= 2) & (comb.loc[:, 5] >= 3), ['vv']] = 1
# print(comb['vv'].sum())
# print(comb.loc[(comb.loc[:, 2] >= 2) & (comb.loc[:, 5] >= 3)])





