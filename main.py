import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import mplfinance as mpf
from datetime import datetime

# function ดึงค่า จาก yfinance
def get_stock_data(stock_symbol):
  try:
    stock = yf.Ticker(stock_symbol)
    info = stock.info

    roa = info.get('returnOnAssets',None)
    roe = info.get('returnOnEquity',None)
    grossProfitMargin = info.get('grossProfitMargin',None)
    debtToEquity = info.get('debtToEquity',None)
    operatingCashflow = info.get('operatingCashflow',None)

    return roa*100,roe*100,grossProfitMargin,debtToEquity,operatingCashflow
  except Exception as e:
    return 'None','None','None','None','None'
  
# function สร้าง กราฟ แท่งเทียน
def plot_graph(stock_symbol,timeframe):
  try:
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period=timeframe)

    if data.empty:
      messagebox.showerror("Error ครับพี่")
      return
    mpf.plot(data,type='candle',figsize=(10,6),title=f'{stock_symbol} timeframe ({timeframe})',style='charles')

  except Exception as e:
    messagebox.showerror("Error ครับพี่")

# function แสดง ข้อมูล หุ้น
def show_stock_info():

  stock_symbol = entry.get()

  if stock_symbol:
    roa,roe,grossProfitMargin,debtToEquity,operatingCashflow = get_stock_data(stock_symbol)
    result_text = f"""
    Stock: {stock_symbol}
    ROA: {roa} 
    ROE: {roe}
    Gross Profit Margin (%): {grossProfitMargin}
    Debt-to-Equity Ratio: {debtToEquity}
    Operating Cash Flow: {operatingCashflow} """

    result_label.config(text=result_text)
  
    timeframe = timeframe_var.get()
    plot_graph(stock_symbol, timeframe)

  else:
        messagebox.showwarning("Input Error", "ลองกรอก ชื่อหุ้น ใหม่ครับพี่")



root = tk.Tk()
root.title("Stock Information and Candlestick Chart")

# ใส่ชื่อหุ้น
label = tk.Label(root, text="Enter Stock Symbol:")
label.pack()

entry = tk.Entry(root)
entry.pack()

# ปุ่มดึงข้อมูล
fetch_button = tk.Button(root, text="Fetch Data", command=show_stock_info)
fetch_button.pack()

# แสดงข้อมูล
result_label = tk.Label(root, text="", justify=tk.LEFT)
result_label.pack()

#  Timeframe
timeframe_var = tk.StringVar(value='1d')  
timeframe_label = tk.Label(root, text="Select Timeframe:")
timeframe_label.pack()

timeframe_menu = tk.OptionMenu(root, timeframe_var, '1m', '5m', '15m', '30m',  '1h',  '4h', '1d',  '1wk', '1mo', '3mo', '6mo', '1y','3y','5y')
timeframe_menu.pack() ,


root.mainloop()  