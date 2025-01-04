import tushare as ts
import pandas as pd

# 设置tushare的token，替换为你自己申请到的token
ts.set_token('5c67d5a015299c0b6e264c97a637e67d2e8681c42dd983b71d4b0c00')
pro = ts.pro_api()

# 获取交易日历，确定有效的交易日范围
trade_cal_df = pro.trade_cal(exchange='', start_date='20250101', end_date='20250105')  
valid_dates = trade_cal_df[trade_cal_df['is_open'] == 1]['cal_date'].tolist()

for date in valid_dates:
    # 获取指定交易日的股票日线行情数据
    daily_data = pro.daily(trade_date=date)
    # 对于主板股票（一般涨跌幅限制为10%左右，这里简单以大于等于9.9%近似判断涨停）
    zt_main_board = daily_data[(daily_data['pct_chg'] >= 9.9) & (daily_data['ts_code'].str.startswith(('60', '00')))]
    # 对于科创板股票（代码以688开头，涨跌幅限制一般为20%左右，这里简单以大于等于19.9%近似判断涨停）
    zt_sci_tech_board = daily_data[(daily_data['pct_chg'] >= 19.9) & (daily_data['ts_code'].str.startswith('688'))]
    # 对于创业板股票（代码以300开头，涨跌幅限制一般为20%左右，这里简单以大于等于19.9%近似判断涨停）
    zt_growth_board = daily_data[(daily_data['pct_chg'] >= 19.9) & (daily_data['ts_code'].str.startswith('300'))]

    # 合并各板块的涨停板数据
    zt_data = pd.concat([zt_main_board, zt_sci_tech_board, zt_growth_board])
    print(f"{date}的涨停板数据如下：")
    print(zt_data[['ts_code', 'name', 'close', 'pct_chg']])