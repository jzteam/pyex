#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import urllib.request,urllib.parse
import ssl,re,os,hashlib
from io import StringIO
from io import BytesIO
import gzip as gzip_mod
import zlib as zlib_mod

ssl._create_default_https_context = ssl._create_unverified_context


def gzip(data):
    buf = BytesIO(data)
    f = gzip_mod.GzipFile(fileobj=buf)
    return f.read()

def deflate(data):
    try:
        return zlib_mod.decompress(data, -zlib_mod.MAX_WBITS)
    except zlib_mod.error:
        return zlib_mod.decompress(data)


# get请求
def get(url,params):
	# 构造请求头
	headers = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'useGzip': 'false',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	# 拼接queryString
	if params:
		arr = []
		for key in params.keys():
			arr.append("%s=%s" % (key,params[key]))
		queryString = "&".join(arr)
		url = "%s?%s" % (url, queryString)
	print("url=%s" % url)
	# 发送get请求：data=None表示get请求
	req=urllib.request.Request(url,None,headers)
	httpResponse = urllib.request.urlopen(req)
	# 获取响应信息
	content = httpResponse.read()
	encoding = httpResponse.info().get('Content-Encoding')
	# 解压缩
	if encoding == 'gzip':
		content = gzip(content)
	elif encoding == 'deflate':
		content = deflate(content)
	return content.decode('utf-8')

# post请求
def post(url,params):
	# 构造请求头
	headers = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'useGzip': 'false',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	# 处理请求参数
	data = bytes(urllib.parse.urlencode(params),encoding='utf-8')
	print("url=%s, params=%s" % (url, params))
	# 发送post请求：data不为None，表示post请求
	req=urllib.request.Request(url,data,headers)
	httpResponse = urllib.request.urlopen(req)
	# 获取响应信息
	content = httpResponse.read()
	encoding = httpResponse.info().get('Content-Encoding')
	# 解压缩
	if encoding == 'gzip':
		content = gzip(content)
	elif encoding == 'deflate':
		content = deflate(content)
	return content.decode('utf-8')



if __name__ == "__main__":
	html = crawler("https://www.okex.com/api/v1/ticker.do", sign({"symbol":"okb_usdt"}))
	print(html)

