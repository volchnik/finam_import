import urllib2
import datetime
import os
import os.path
import json
import sys
from package import package_quote


def get_stock_key_alt(code_stock, date):
  if code_stock == 'RI' or code_stock == 'Si' or code_stock == 'SP' or code_stock == 'GZ' or code_stock == 'LK':
    if 12 <= date.month or date.month <= 2:
      stock_postfix = "H"
    elif 3 <= date.month <= 5:
      stock_postfix = "M"
    elif 6 <= date.month <= 8:
      stock_postfix = "U"
    else:
      stock_postfix = "Z"

    return code_stock + stock_postfix + get_date_postfix(date)[1:]
  else:
    return code_stock


def get_stock_key(code_stock, date):
  if code_stock == 'RI' or code_stock == 'Si' or code_stock == 'SP' or code_stock == 'GZ' or code_stock == 'LK':
    if 12 <= date.month or date.month <= 2:
      stock_postfix = "3"
    elif 3 <= date.month <= 5:
      stock_postfix = "6"
    elif 6 <= date.month <= 8:
      stock_postfix = "9"
    else:
      stock_postfix = "12"

    return code_stock + "-" + stock_postfix + "." + get_date_postfix(date)
  else:
    return code_stock


def get_date_postfix(date):
  return (str(date.year)[2:]) if (date.month <= 11) else str(int(str(date.year)[2:]) + 1).zfill(2)


def download_stock(code_stock, date, json_charts_data):
  code_stock_key = get_stock_key(code_stock, date)
  code_stock_key_alt = get_stock_key_alt(code_stock, date)

  url = 'http://export.finam.ru/{5}_{0}{1}{3}_{0}{1}{3}.txt?market=17&em={6}&code={5}&df={4}&mf={2}&yf=20{0}&from={3}.{1}.20{0}&dt={4}&mt={2}&yt=20{0}&to={3}.{1}.20{0}&p=1&f={5}_{0}{1}{3}_{0}{1}{3}&e=.txt&cn={5}&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=3&sep2=1&datf=6'.format(
    str(date.year)[2:], str(date.month).rjust(2, '0'), date.month - 1, str(date.day).rjust(2, '0'), date.day,
    code_stock_key, json_charts_data[code_stock_key_alt])

  print "downloading " + url

  request = urllib2.Request(url, headers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8,ru;q=0.6",
    "Connection": "keep-alive",
    "Host": "195.128.78.52",
    "Referer": "http://www.finam.ru/profile/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
  })
  data = urllib2.urlopen(request).read()
  if not os.path.exists("./data/" + code_stock):
    os.makedirs("./data/" + code_stock)
  file_name = "{3}/{4}_{0}{1}{2}_{0}{1}{2}.txt".format(str(date.year)[2:], str(date.month).rjust(2, '0'),
                                                       str(date.day).rjust(2, '0'), code_stock, code_stock_key_alt)
  with open('./data/' + file_name, "wb") as code:
    code.write(data)
  if os.path.getsize('./data/' + file_name) < 1000:
    os.remove('./data/' + file_name)
  else:
    package_quote(file_name, None)
    if code_stock == "RI":
      package_quote(file_name, True)
      package_quote(file_name, False)
  return


with open('icharts.json') as json_data_file:
  json_charts_data = json.load(json_data_file)

json_charts_data_dict = dict(zip(json_charts_data["aEmitentCodes"], json_charts_data["aEmitentIds"]))

date_start = datetime.date(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])).toordinal()
quote_list = sys.argv[1].split(',')
for current_date in range(date_start, date_start + int(sys.argv[5])):
  for quote in quote_list:
    download_stock(quote, datetime.date.fromordinal(current_date), json_charts_data_dict)
