import os
import json
import sys
import csv
import shutil
'''
Once we have generated the resource sharing results, 
you can run this script, with one argument (the output directory)
to get a summary of lut, dsp, register, and mux usage. Currently 
some of this script is hard coded (e.g., the global `files` list)
so I should try to improve it. 
'''

supported_files = ["google", "lenet", "alex", "squeeze", "vgg", "mobile"]

def rename_file(old_file_name):
  for possible_new_name in supported_files:
    if possible_new_name in old_file_name:
      return possible_new_name 
  return old_file_name 

if __name__ == "__main__":
    assert (len(sys.argv) == 2), "please provide an input json file name"
    json_data = json.load(open(sys.argv[1]))
    
    OUTPUT_FILE = json_data["output_file"]
    files = json_data["files"] 
    stats = json_data["stats"]
    
    csv_writer = csv.writer(open(f"{OUTPUT_FILE}", 'w'))
    header = ['setting'] + stats
    csv_writer.writerow(header)
    
    for f in files:
        with open(f) as json_file:  
          json_data = json.load(json_file)
          for share_setting in json_data:
            for bound_setting in json_data[share_setting]:
              cur_row = [f"{rename_file(f)}_{share_setting}_{bound_setting}"]
              for stat in stats:
                cur_row += [json_data[share_setting][bound_setting][stat]]
              csv_writer.writerow(cur_row)
            