import pandas as pd
from yahoo_fin import stock_info as si
from yahoo_fin import news
import requests
from io import StringIO

#從yahoo套件獲取股票資訊

def get_quote_table(ticker):
    site = f"https://finance.yahoo.com/quote/{ticker}"
    tables = pd.read_html(StringIO(requests.get(site).text))

    # 使用 pd.concat 代替 append
    if len(tables) > 1:
        data = pd.concat([tables[0], tables[1]], axis=0)
    else:
        data = tables[0]
    
    data.columns = ["Attribute", "Value"]
    data = data.set_index("Attribute")
    return data.to_dict()["Value"]

def get_stock_data(ticker):
    try:
        quote_table = get_quote_table(ticker)
        return quote_table
    except Exception as e:
        print(f"Error getting stock data for {ticker}: {e}")
        return None

# 示例：获取苹果公司的实时报价信息
stock_ticker = "AAPL"
quote_table = get_stock_data(stock_ticker)
if quote_table is not None:
    print("实时报价信息：")
    for key, value in quote_table.items():
        print(f"{key}: {value}")

# def get_stock_data(ticker):
#     # 获取基本面信息
#     stock_info = si.get_quote_table(ticker)
#     print("基本面信息：")
#     for key, value in stock_info.items():
#         print(f"{key}: {value}")

#     # 获取新闻
#     stock_news = news.get_yf_rss(ticker)
#     print("\n新闻：")
#     for news_item in stock_news:
#         print(f"标题: {news_item['title']}")
#         print(f"链接: {news_item['link']}")
#         print(f"发布时间: {news_item['pubDate']}\n")

# # 示例：获取苹果公司数据
# get_stock_data("AAPL")