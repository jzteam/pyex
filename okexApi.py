#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import re,os,hashlib
from HttpUtil import get,post
from test import Properties



# md5加密
def md5(s):
	hl = hashlib.md5()
	# 此处必须声明encode，否则报错： Unicode-objects must be encoded before hashing
	hl.update(s.encode(encoding='utf-8'))
	digest = hl.hexdigest()
	# 返回全大写字母
	return digest.upper()

prop = Properties()
api_key=prop.api_key
secret_key=prop.secret_key

# 增加签名参数
def sign(paramDict):
	paramDict["api_key"]=api_key
	arr = []
	for key in paramDict.keys():
		arr.append("%s=%s" % (key,paramDict[key]))
	arr = sorted(arr, key=str.lower)
	print("arr=%s" % arr)
	s = "&".join(arr)
	result = "%s&secret_key=%s" % (s, secret_key)
	signStr = md5(result)
	paramDict["sign"] = signStr
	return paramDict

#获取OKEX现货行情信息
def ticker(symbol = ''):
    TICKER_RESOURCE = "https://www.okex.com/api/v1/ticker.do"
    params = {}
    if symbol:
        params["symbol"] = symbol
    return get(TICKER_RESOURCE,sign(params))

#获取OKEX现货市场深度信息
def depth(symbol = ''):
    DEPTH_RESOURCE = "https://www.okex.com/api/v1/depth.do"
    params={}
    if symbol:
        params["symbol"] = symbol
    return get(DEPTH_RESOURCE,sign(params)) 

#获取OKEX现货历史交易信息
def trades(symbol = ''):
    TRADES_RESOURCE = "https://www.okex.com/api/v1/trades.do"
    params={}
    if symbol:
        params["symbol"] = symbol
    return get(TRADES_RESOURCE,sign(params))

#获取用户现货账户信息
def userinfo():
    USERINFO_RESOURCE = "https://www.okex.com/api/v1/userinfo.do"
    params={}
    return post(USERINFO_RESOURCE,sign(params))

#现货交易
def trade(symbol,tradeType,price='',amount=''):
    TRADE_RESOURCE = "https://www.okex.com/api/v1/trade.do"
    params = {
        'symbol':symbol,
        'type':tradeType
    }
    if price:
        params['price'] = price
    if amount:
        params['amount'] = amount
        
    return post(TRADE_RESOURCE,sign(params))

#现货批量下单 -- 待验证
def batchTrade(symbol,tradeType,orders_data):
    BATCH_TRADE_RESOURCE = "https://www.okex.com/api/v1/batch_trade.do"
    params = {
        'symbol':symbol,
        'type':tradeType,
        'orders_data':orders_data
    }
    return post(BATCH_TRADE_RESOURCE,sign(params))

#现货取消订单
def cancelOrder(symbol,orderId):
    CANCEL_ORDER_RESOURCE = "https://www.okex.com/api/v1/cancel_order.do"
    params = {
         'symbol':symbol,
         'order_id':orderId
    }
    return post(CANCEL_ORDER_RESOURCE,sign(params))

#现货订单信息查询
def orderinfo(symbol,orderId):
     ORDER_INFO_RESOURCE = "https://www.okex.com/api/v1/order_info.do"
     params = {
         'symbol':symbol,
         'order_id':orderId
     }
     return post(ORDER_INFO_RESOURCE,sign(params))

#现货批量订单信息查询 -- 待验证
def ordersinfo(symbol,orderId,tradeType):
     ORDERS_INFO_RESOURCE = "https://www.okex.com/api/v1/orders_info.do"
     params = {
         'symbol':symbol,
         'order_id':orderId,
         'type':tradeType
     }
     return post(ORDERS_INFO_RESOURCE,sign(params))

#现货获得历史订单信息
def orderHistory(symbol,status,currentPage,pageLength):
       ORDER_HISTORY_RESOURCE = "https://www.okex.com/api/v1/order_history.do"
       params = {
          'symbol':symbol,
          'status':status,
          'current_page':currentPage,
          'page_length':pageLength
       }
       return post(ORDER_HISTORY_RESOURCE,sign(params))



if __name__ == "__main__":
    product = "okb_usdt"
	#tickerInfo = ticker(product)
	#print(tickerInfo)
    #depthInfo = depth(product)
    #print(depthInfo)
    # tradesInfo = trades(product)
    # print(tradesInfo)
    # userInfo = userinfo()
    # print(userInfo)
    # tradeInfo = trade(product,"buy",price='3.85',amount='1')
    # print(tradeInfo)
    # cancelOrderInfo = cancelOrder(product, 521878231)
    # print(cancelOrderInfo)
    # orderInfo = orderinfo(product, 521878231)
    # print(orderInfo)
    orderHistoryInfo = orderHistory(product, -1, 1, 10)
    print(orderHistoryInfo)

