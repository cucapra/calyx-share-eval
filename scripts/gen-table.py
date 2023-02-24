import os
import json
import sys
import csv
import shutil
from pathlib import Path 
from resource_usage import simplify_file_name
'''
Once we have generated the resource sharing results, 
you can run this script, with one argument (the output directory)
to get a table of each of the results. 

run scripts/gen-table.py <path/to/json> to get the resource results 

The json should contain the following information: 

"files": the path to the files 
"stats": list of stats you want to collect. Include the word "all" in your list 
if you want to collect all stats 
"output_file": the file to write the csv to
'''

def flatten(l):
  '''
  source: https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
  '''
  return [item for sublist in l for item in sublist]

def get_all_stats(files):
  '''
  returns a list of keys for all possible stats that got collected 
  '''
  for f in files:
    with open(f) as json_file:  
      json_data = json.load(json_file)
      for share_setting in json_data:
        for bound_setting in json_data[share_setting]:
          # we just need to get to a place where we can have a list of all possible 
          # stats (i.e., dsp, lut, registers, etc.) to collect 
          return list(json_data[share_setting][bound_setting])
            

if __name__ == "__main__":
    assert (len(sys.argv) == 2), "please provide an input json file name"
    json_data = json.load(open(sys.argv[1]))
    
    OUTPUT_FILE = json_data["output_file"]
    my_path = '/'.join(OUTPUT_FILE.split('/')[0:-1])
    if (not my_path == '') and (not os.path.exists(my_path)):
      os.makedirs(my_path)
    files = json_data["files"] 
    stats = json_data["stats"]
    
    if "all" in stats:
      # update stats to be all possible stats if that's what we want to collect 
      stats = get_all_stats(files)
  
    csv_writer = csv.writer(open(f"{OUTPUT_FILE}", 'w'))
    header = ['setting']
    # for just the first iteration through a json file, we will need to collect 
    # information for the header. After this it won't be necessary 
    need_header_info = True 
    
    rows = []
    
    for f in files:
      with open(f) as json_file:  
        json_data = json.load(json_file)
        for share_setting in json_data:
          cur_row = [f"{simplify_file_name(f)}_{share_setting}"]
          # need to keep cur_row_data as nested list so it appears in a more 
          # intuitive order in the csv file 
          cur_row_data = list(([] for _ in stats))
          header_data = list(([] for _ in stats))
          for bound_setting in json_data[share_setting]:
            for idx,stat in enumerate(stats):
              if need_header_info:
                header_data[idx].append(stat + "_" + bound_setting)
              cur_row_data[idx].append(json_data[share_setting][bound_setting][stat]) 
          cur_row += flatten(cur_row_data)
          rows.append(cur_row)
          if need_header_info:
            # the csv file only needs one header, so once we have the header info 
            # needed, we don't need to collect it again 
            header += flatten(header_data)
            need_header_info = False 

    rows.insert(0, header)
    for line in rows:
      csv_writer.writerow(line)
            