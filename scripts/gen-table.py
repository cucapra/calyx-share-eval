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
      
def get_header(files, stats):
  '''
  header data should be organized by 1) stats and 2) bound 
  For example: lut_1,1, lut_4,4, lut_-1,-1, dsp_1,1, etc. 
  Assumes each file contains the same stats *in the same order* 
  Might be wise to change script so this doesn't happen
  '''
  header_data = ["design/resource"]
  for f in files:
    with open(f) as json_file: 
      json_data = json.load(json_file) 
      for share_setting in json_data:
        data_by_bound = json_data[share_setting]
        for bound_setting in data_by_bound:
            header_data.append(share_setting + "_" + bound_setting)
    return header_data

if __name__ == "__main__":
    assert (len(sys.argv) == 2), "please provide an input json file name"
    table_info = json.load(open(sys.argv[1]))
    files = table_info["files"] 
    stats = table_info["stats"]
    if "all" in stats:
      # update stats to be all possible stats if that's what we want to collect 
      stats = get_all_stats(files)
    # makes path to file if it doesn't exist
    path = table_info["output_path"]
    if (not path == '') and (not os.path.exists(path)):
      os.makedirs(path) 
    OUTPUT_FILE = os.path.join(path, table_info["output_file"])
        
    # rows should start with the header 
    rows = [get_header(files, stats)]
    
    for f in files:
      with open(f) as json_file:  
        json_data = json.load(json_file)
        for stat in stats:
          cur_row = [f"{simplify_file_name(f)}_{stat}"]
          for share_setting in json_data:
            data_by_bound = json_data[share_setting]
            for bound_setting in data_by_bound:
                cur_row.append(json_data[share_setting][bound_setting][stat]) 
          rows.append(cur_row)
    
    csv_writer = csv.writer(open(f"{OUTPUT_FILE}", 'w'))
    # write each line in rows to file 
    for line in rows:
      csv_writer.writerow(line)