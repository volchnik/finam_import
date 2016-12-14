import urllib2
import datetime
import os
import os.path
import json
import sys
from package import package_quote

with open('icharts.json') as json_data_file:
  json_charts_data = json.load(json_data_file)

#json_charts_data_dict = dict(zip(json_charts_data["aEmitentCodes"], json_charts_data["aEmitentIds"]))
json_charts_data_dict = dict(zip(json_charts_data["aEmitentIds"], json_charts_data["aEmitentCodes"]))

#print json_charts_data_dict['SPFB.Si']
print json_charts_data_dict[420658]