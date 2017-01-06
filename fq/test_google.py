import requests
 
proxies = {
  "http": "127.0.0.1:8087",
  "https": "127.0.0.1:8087",
}

try: 
	r=requests.get("http://www.baidu.com", proxies=proxies)
	print(r.status_code)
	print(r.text)
except Exception as e:
	print(e)	