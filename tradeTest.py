#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import urllib.request,urllib.parse
import ssl,re,os,hashlib
from io import StringIO
from io import BytesIO
import gzip as gzip_mod
import zlib as zlib_mod
from test import Properties

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

def md5(s):
	hl = hashlib.md5()
	# Tips
	# 此处必须声明encode
	# 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
	hl.update(s.encode(encoding='utf-8'))
	digest = hl.hexdigest()
	print('MD5加密前为 ：' + s)
	print('MD5加密后为 ：' + digest)
	return digest.upper()

def crawler(url, data=None):
	# 构造请求头
	data = bytes(urllib.parse.urlencode(data),encoding='utf-8')
	# arr = []
	# for key in data.keys():
	# 	arr.append("%s=%s" % (key,data[key]))
	# s = "&".join(arr)
	# url = "%s?%s" % (url, s)

	headers = {
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
		'useGzip': 'false',
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	print("url=%s" % url)
	req=urllib.request.Request(url,data,headers)
	httpResponse = urllib.request.urlopen(req)
	# 所有信息
	content = httpResponse.read()
	encoding = httpResponse.info().get('Content-Encoding')

	if encoding == 'gzip':
		content = gzip(content)
	elif encoding == 'deflate':
		content = deflate(content)
	print('encoding=%s' % encoding)
	return content.decode('utf-8')

prop = Properties()
api_key=prop.api_key
secret_key=prop.secret_key

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


if __name__ == "__main__":
	html = crawler("https://www.okex.com/api/v1/ticker.do", sign({"symbol":"okb_usdt"}))
	print(html)

