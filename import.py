import urllib2
import datetime
import os
import os.path
import json
 
def downloadStock(code_stock, date, json_charts_data):
  if 12 <= date.month or date.month <= 2 :
    stock_postfix = "H";
  elif 3 <= date.month <= 5:
    stock_postfix = "M";
  elif 6 <= date.month <= 8:
    stock_postfix = "U";
  else:
    stock_postfix = "Z";
    
  code_stock_key = code_stock + stock_postfix + str(date.year)[3:]

  url = 'http://195.128.78.52/{5}_{0}{1}{3}_{0}{1}{3}.txt?market=17&em={6}&code={5}&df={4}&mf={2}&yf=20{0}&from={3}.{1}.20{0}&dt={4}&mt={2}&yt=20{0}&to={3}.{1}.20{0}&p=1&f={5}_{0}{1}{3}_{0}{1}{3}&e=.txt&cn={5}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=3&sep2=1&datf=6'.format(str(date.year)[2:], str(date.month).rjust(2, '0'), date.month - 1, str(date.day).rjust(2, '0'), date.day, code_stock_key, json_charts_data[code_stock_key])
   
  print "downloading " + url

  request = urllib2.Request(url, headers={
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
  "Accept-Encoding":"gzip, deflate, sdch",
  "Accept-Language":"en-US,en;q=0.8,ru;q=0.6",
  "Connection":"keep-alive",
  "Host":"195.128.78.52",
  "Referer":"http://www.finam.ru/profile/",
  "Upgrade-Insecure-Requests":"1",
  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  })
  data = urllib2.urlopen(request).read()
  if not os.path.exists("./data/" + code_stock):
    os.makedirs("./data/" + code_stock)
  file_name = "./data/{3}/{4}_{0}{1}{2}_{0}{1}{2}.txt".format(str(date.year)[2:], str(date.month).rjust(2, '0'), str(date.day).rjust(2, '0'), code_stock, code_stock + stock_postfix + str(date.year)[3:])
  with open(file_name, "wb") as code :
    code.write(data)
  if os.path.getsize(file_name) < 1000:
    os.remove(file_name)
  return

with open('icharts.json') as json_data_file:    
  json_charts_data = json.load(json_data_file)
  
json_charts_data_dict = dict(zip(json_charts_data["aEmitentCodes"], json_charts_data["aEmitentIds"]))

date_start = datetime.date(2010, 3, 12).toordinal();
for current_date in range(date_start, date_start + 6):
  downloadStock("RI", datetime.date.fromordinal(current_date), json_charts_data_dict);