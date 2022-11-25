from resource_usage import simplify_file_name
import os 
import json 
import sys 

if __name__ == "__main__":
  assert (len(sys.argv) == 2), "please provide an input json file name"
  
   # reading the json file 
  json_data = json.load(open(sys.argv[1]))
  files = json_data["files"] 
  
  for f in files:
    os.system(f'tmux new-session -A -s {simplify_file_name(f)}\; send-keys "python3 scripts/resource_usage.py {f}" Enter')
    
    
    
    
  

