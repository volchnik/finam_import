import gzip
import collections
import sys
import os
import os.path
import git

def package_quote(quote_path, use_max):
  quote_dict = {}
  volume_dict = {}
  with gzip.open('data/' + quote_path, 'r') as f:
    for line in f:
      line_list = line.rstrip('\n').split(';')
      if line_list[3] < '180000':
        if use_max is None:
          quote_dict[line_list[2] + line_list[3]] = float(line_list[4]);
        elif use_max:
          if line_list[2] + line_list[3] in quote_dict:
            quote_dict[line_list[2] + line_list[3]] = max(float(line_list[4]), quote_dict[line_list[2] + line_list[3]])
          else:
            quote_dict[line_list[2] + line_list[3]] = float(line_list[4])
        else:
          if line_list[2] + line_list[3] in quote_dict:
            quote_dict[line_list[2] + line_list[3]] = min(float(line_list[4]), quote_dict[line_list[2] + line_list[3]])
          else:
            quote_dict[line_list[2] + line_list[3]] = float(line_list[4])

        volume_dict[line_list[2] + line_list[3]] = (volume_dict[line_list[2] + line_list[3]] + int(line_list[5])) \
          if (line_list[2] + line_list[3] in volume_dict) else int(line_list[5]);

  dir = quote_path.split('/')[0] + ("" if use_max is None else ("_MAX" if use_max else "_MIN"));

  quote_path_array = quote_path.split('/')[1:]
  if use_max is not None:
    quote_path_array_sub = quote_path_array[0].split('_')
    quote_path_array_sub[0] += "_MAX" if use_max else "_MIN"
    quote_path_array[0] = '_'.join(quote_path_array_sub)

  quote_path = '/'.join(quote_path_array)

  if not os.path.exists("stock_quotes/data_seconds/" + dir):
    os.makedirs("stock_quotes/data_seconds/" + dir)

  write_path = 'stock_quotes/data_seconds/' + dir + "/" + quote_path;
  print "packaging " + write_path
  with gzip.open(write_path, 'w') as f:
    for key, val in sorted(quote_dict.items()):
      f.write(key[:8] + ';' + key[8:] + ';' + str(val) + ';' + str(volume_dict[key]) + '\n')
  repo = git.Repo('stock_quotes/')
#  print repo.git.add('data_seconds/' + quote_path)
#  print repo.git.commit(m='added ' + '/data_seconds/' + quote_path)
