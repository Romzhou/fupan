import pywencai
import pandas as pd

# 列名与数据对其显示
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', 100)

date = "20240821"
param = "{date}涨停，非涉嫌信息披露违规且非立案调查且非ST，非科创板，非北交所"
df = pywencai.get(query=param, sort_key='成交金额', sort_order='desc')

# 打印原始数据
print(df)

# 选择特定列
selected_columns = ('股票代码', '股票简称', '最新价', '最新涨跌幅', '首次涨停时间(' + date + ')', '连续涨停天数(' + date + ')','涨停原因类别(' + date + ')','a股市值(不含限售股)(' + date + ')','涨停类型(' + date + ')')
jj_df = df[selected_columns]

# 按照'连板数'列进行降序排序
sorted_temp_df = jj_df.sort_values(by='连续涨停天数(' + date + ')', ascending=False)

# 输出排序后的DataFrame
print(sorted_temp_df)

# 保存到Excel
spath = f"./{date}涨停wencai.xlsx"
df.to_excel(spath, engine='xlsxwriter')
sorted_temp_df_path = f"./{date}涨停排序wencai.xlsx"
sorted_temp_df.to_excel(sorted_temp_df_path, engine='xlsxwriter')