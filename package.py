import gzip
import collections
import sys
import os
import os.path
import git

def package_quote(quote_path):
  print "packaging " + quote_path
  quote_dict = {}
  volume_dict = {}
  with gzip.open('data/' + quote_path, 'r') as f:
    for line in f:
      line_list = line.rstrip('\n').split(';')
      quote_dict[line_list[2] + line_list[3]] = float(line_list[4]);
      volume_dict[line_list[2] + line_list[3]] = (volume_dict[line_list[2] + line_list[3]] + int(line_list[5])) if (line_list[2] + line_list[3] in volume_dict) else int(line_list[5]);

  if not os.path.exists("stock_quotes/data_seconds/" + quote_path.split('/')[0]):
    os.makedirs("stock_quotes/data_seconds/" + quote_path.split('/')[0])
  with gzip.open('stock_quotes/data_seconds/' + quote_path, 'w') as f:
    for key, val in sorted(quote_dict.items()):
      f.write(key[:8] + ';' + key[8:] + ';' + str(val) + ';' + str(volume_dict[key]) + '\n')
  repo = git.Repo('stock_quotes/')
  print repo.git.add('data_seconds/' + quote_path)
  print repo.git.commit(m='added ' + '/data_seconds/' + quote_path)